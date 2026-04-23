import tkinter as tk
from tkinter import messagebox

def calculate_tax_amount(income, salaried=True):
    info=""

    if salaried:
        income-=75000
        info+=f"Standard Deduction: ₹75,000\nTaxable Income: ₹{income:,.0f}\n\n"

    if income<=0:
        return 0, info+"No taxable income."

    slabs=[
        (400000,0),(400000,.05),(400000,.10),
        (400000,.15),(400000,.20),(400000,.25),
        (float('inf'),.30)
    ]

    tax=0
    original_income=income

    for i,(limit,rate) in enumerate(slabs,1):
        if income<=0:
            break

        amt=min(income,limit)
        slab_tax=amt*rate
        tax+=slab_tax

        info+=f"Slab {i}: ₹{amt:,.0f} @ {int(rate*100)}% = ₹{slab_tax:,.2f}\n"
        income-=amt

    if original_income<=1200000:
        rebate=min(tax,60000)
        tax-=rebate
        info+=f"\nRebate: -₹{rebate:,.2f}"

    cess=tax*.04
    total=tax+cess

    info+=f"\nCess (4%): ₹{cess:,.2f}"
    info+=f"\n---------------------"
    info+=f"\nTotal Tax: ₹{total:,.2f}"

    return round(total,2),info


def set_income(val):
    income_entry.delete(0,tk.END)
    income_entry.insert(0,val)


def calculate():
    try:
        income=float(income_entry.get())
        if income<0:
            raise ValueError

        tax,details=calculate_tax_amount(
            income,
            emp_type.get()=="Salaried"
        )

        monthly_tax=tax/12
        take_home=income-tax

        result_label.config(
            text=f"Yearly Tax: ₹{tax:,.2f}\n"
                 f"Monthly Tax: ₹{monthly_tax:,.2f}\n"
                 f"Take Home: ₹{take_home:,.2f}"
        )

        breakdown.delete("1.0",tk.END)
        breakdown.insert(tk.END,details)

    except:
        messagebox.showerror(
            "Error",
            "Enter valid income"
        )


# ---------------- UI ---------------- #

root=tk.Tk()
root.title("Income Tax Calculator FY 2025-26")
root.geometry("540x620")
root.configure(bg="#eef4f8")
root.resizable(False,False)

card=tk.Frame(root,bg="white",bd=2,relief="groove")
card.pack(padx=20,pady=15,fill="both",expand=True)

tk.Label(
    card,
    text="Income Tax Calculator",
    font=("Segoe UI",18,"bold"),
    bg="white",
    fg="#2c3e50"
).pack(pady=12)

tk.Label(
    card,
    text="Enter Annual Income (₹)",
    font=("Segoe UI",11),
    bg="white"
).pack()

income_entry=tk.Entry(
    card,
    font=("Segoe UI",13),
    justify="center",
    width=18
)
income_entry.pack(pady=8)

# Presets
preset_frame=tk.Frame(card,bg="white")
preset_frame.pack()

for amt in [500000,1000000,1500000,2000000]:
    tk.Button(
        preset_frame,
        text=f"₹{amt//100000}L",
        command=lambda a=amt:set_income(a),
        bg="#dfe9f3",
        width=7
    ).pack(side="left",padx=5)

# Employee Type
emp_type=tk.StringVar(value="Salaried")

type_frame=tk.Frame(card,bg="white")
type_frame.pack(pady=15)

for txt in ["Salaried","Business"]:
    tk.Radiobutton(
        type_frame,
        text=txt,
        variable=emp_type,
        value=txt,
        bg="white"
    ).pack(side="left",padx=15)

tk.Button(
    card,
    text="Calculate Tax",
    command=calculate,
    font=("Segoe UI",12,"bold"),
    bg="#4CAF50",
    fg="white",
    padx=18,
    pady=6
).pack(pady=10)

result_label=tk.Label(
    card,
    text="",
    font=("Segoe UI",11,"bold"),
    fg="#1565C0",
    bg="#f4f9ff",
    width=38,
    height=3
)
result_label.pack(pady=10)

tk.Label(
    card,
    text="Tax Breakdown",
    font=("Segoe UI",11,"bold"),
    bg="white"
).pack()

frame=tk.Frame(card)
frame.pack(pady=8)

scroll=tk.Scrollbar(frame)
scroll.pack(side="right",fill="y")

breakdown=tk.Text(
    frame,
    width=52,
    height=11,
    font=("Consolas",9),
    yscrollcommand=scroll.set
)
breakdown.pack()

scroll.config(command=breakdown.yview)

root.mainloop()