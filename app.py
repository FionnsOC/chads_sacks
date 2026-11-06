from flask import Flask, render_template, request, redirect, url_for
from calc import calculate, to_coins
from db import close_db, init_db, save_payout, get_balances, get_payouts
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from harptos import MONTHS, YEARS, is_valid, format_date


app = Flask(__name__)
app.teardown_appcontext(close_db)
app.jinja_env.filters["coins"] = to_coins    # lets templates write {{ value | coins }}
app.jinja_env.globals["harptos"] = format_date   # {{ harptos(year, month, day) }} in templates
app.secret_key = "any-long-random-text-you-like"   # signs the login cookie

USERNAME = "chad"
PASSWORD = "sacks123"

with app.app_context():
    init_db()

# Public Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# Private Routes
@app.route("/how_it_works")
def how_it_works():
    bags = 12   # example value
    per_pc, per_employee, fund = calculate(bags)
    return render_template("how_it_works.html", bags=bags,
                           per_pc=to_coins(per_pc),
                           per_employee=to_coins(per_employee),
                           fund=to_coins(fund))

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = None
    error = None
    bags = None

    if request.method == "POST":
        try:
            bags = int(request.form["bags"])
            if bags < 0:
                raise ValueError
        except ValueError:
            error = "Please enter a whole number, 0 or higher."
        else:
            per_pc, per_employee, fund = calculate(bags)   # the "recalculate on the server" step
            result = {
                "pc": to_coins(per_pc),
                "employee": to_coins(per_employee),
                "fund": to_coins(fund),
            }
            if request.form.get("action") == "save":
                try:
                    dr_year = int(request.form["dr_year"])
                    dr_month = int(request.form["dr_month"])
                    dr_day = int(request.form["dr_day"])
                    if not is_valid(dr_year, dr_month, dr_day):
                        raise ValueError
                except (KeyError, ValueError):
                    error = "Please enter a valid date: a year, a month, and a day from 1 to 30."
                else:
                    save_payout(bags, per_employee, fund, dr_year, dr_month, dr_day)
                    return redirect(url_for("balances"))

    return render_template("calculator.html", result=result, error=error, bags=bags,
                       calendar=MONTHS, years=YEARS, form=request.form)

@app.route("/balances")
#@login_required
def balances():
    payouts = get_payouts()
    valid_ids = {p["id"] for p in payouts}

    choice = request.args.get("payout", "latest")
    if choice.isdigit() and int(choice) in valid_ids:
        payout_id = int(choice)
    else:                                   # "latest", or anything unexpected
        choice = "latest"
        payout_id = payouts[0]["id"] if payouts else None

    current = next((p for p in payouts if p["id"] == payout_id), None)
    return render_template("balances.html", rows=get_balances(payout_id),
                           payouts=payouts, selected=choice, current=current)


# Login and Logout Routes
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == USERNAME and password == PASSWORD:
            session.clear()
            session["logged_in"] = True
            return redirect(url_for("how_it_works"))
        error = "Wrong username or password."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
