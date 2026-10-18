# Chad's Sacks

A small Flask website for our D&D campaign. It has a public page for the business and a login area for the owners and employees, where you can calculate payouts and see how much money each employee and the health/education fund currently has.

This README is a guide to running and using the site. It assumes you already know the business and the game mechanic.

---

## 1. Setup (first time only)

You need Python 3 installed. Open PowerShell in the project folder (`chads_sacks`) and run:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install flask
python seed.py
```

- `python seed.py` creates the database (`business.db`) and adds the 8 employees and the fund. Run it only once. Running it again is harmless, but it will not reset the balances.
- If PowerShell refuses to run the activation script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.

Next time you only need to activate the environment again (`.venv\Scripts\Activate.ps1`) before starting the site.

---

## 2. Starting the site

### Only on your own computer

```powershell
flask --app app run --debug
```

Then open <http://127.0.0.1:5000> in your browser. Stop the server with `Ctrl+C`.

### For the other players (same room or same Wi-Fi)

If your players are in the same room or on the same Wi-Fi (for example at a game night), you can serve the site from your own laptop:

```powershell
flask --app app run --host=0.0.0.0
```

Leave out `--debug` here, because debug mode shouldn't be reachable by other devices.

Then find your laptop's local IP address: run `ipconfig` in PowerShell and look for "IPv4 Address", something like `192.168.1.23`. Your players open `http://192.168.1.23:5000` in their browser (use your own address and keep the `:5000`).

Things to know:

- It only works while the laptop is on and the server is running.
- Windows will probably show a firewall prompt. Allow access for **private** networks.
- It does not work for players joining remotely.
- Only do this on a Wi-Fi you trust (see the login warning below).

---

## 3. Logging in

The pages "How it works", "Calculator" and "Balances" are only visible to logged-in users. Visitors only see "The Business", "Contact" and "Employee Login".

To try all features, click **Employee Login** and use:

| | |
|---|---|
| Username | `chad` |
| Password | `sacks123` |

> **WARNING: This login is for testing only and is not safe.**
> The username and password are hardcoded in `app.py` and are not hashed, so anyone who can read the code can see them. There is one shared account for everyone. Do not reuse a password you use anywhere else, and do not put the site on the public internet in this state.

Use **Logout** (top right of the navigation bar) when you are done, especially on a shared computer.

---

## 4. Using the site

| Page | Who sees it | What it is for |
|---|---|---|
| The Business | Everyone | Information about the business and its employees |
| Contact | Everyone | Address and map |
| How it works | Logged in | The rules of the profit mechanic |
| Calculator | Logged in | Calculate and save payouts |
| Balances | Logged in | Current money of each employee and the fund |

### Calculating a payout

1. Open **Calculator**.
2. Enter the number of bags sold (the result of the d12 roll or rolls).
3. Click **Calculate**. The money per party member, per employee and for the fund is shown in gold, silver and copper (1 GP = 10 SP = 100 CP). Nothing is stored yet.

### Saving a payout

1. Enter the number of bags.
2. Click **Save payout**. The amounts are added to the employees' balances and to the fund, and you are taken to the **Balances** page.

Saving is final in the current version, so check the number before you click. Each click on **Save payout** adds the payout once. Reloading the Balances page does not add anything.

### Reading the balances

**Balances** lists the 8 employees and the fund with their current total in GP, SP and CP. Party members and Stefie are not tracked.

---

## 5. Resetting the data

To start from zero (for example after testing), stop the server, delete the file `business.db`, and run `python seed.py` again.

---

## 6. Troubleshooting

| Problem | Fix |
|---|---|
| `flask` is not recognised | Activate the environment first: `.venv\Scripts\Activate.ps1` |
| `Could not locate a Flask application` | Run the command from inside the `chads_sacks` folder |
| Balances show 0 after saving | Run `python seed.py` once (the employees were missing), then save again |
| Other players cannot open the site | Check you used `--host=0.0.0.0`, the same Wi-Fi, the right IP address, and that the firewall prompt was allowed |
| Page has no styling | Hard refresh the browser with `Ctrl+F5` |
