
"""
flujo_tuberias.py

Programa integrado: flujo hidráulico + representación topográfica (matrices y perfiles)
- Permite introducir una matriz de elevaciones (topografía)
- Extraer un perfil longitudinal (fila o columna) o editarlo manualmente
- Crear varios tramos de tubería (lista) y calcular pérdidas por tramos
- Usa Darcy–Weisbach + Colebrook (iterativo) o Swamee–Jain
- Visualiza mapa de elevaciones (heatmap) y perfil longitudinal (plot)
- Exporta resultados a CSV

Guardar en carpeta: mi_modelado
Ejecutar: python flujo_tuberias.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import math
import csv
import matplotlib.pyplot as plt
from matplotlib import cm
import os

# -----------------------------
# UTILIDADES: parseo y ejemplos
# -----------------------------

def parse_matrix_text(text):
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip() != ""]
    if not lines:
        raise ValueError("No se detectaron datos en la matriz.")
    matrix = []
    ncols = None
    for idx, ln in enumerate(lines):
        parts = ln.replace(',', ' ').split()
        try:
            row = [float(p) for p in parts]
        except ValueError:
            raise ValueError(f"Valor no numérico en la fila {idx+1}: '{ln}'")
        if ncols is None:
            ncols = len(row)
        elif len(row) != ncols:
            raise ValueError(f"Inconsistencia en número de columnas (fila {idx+1}).")
        matrix.append(row)
    return np.array(matrix, dtype=float)


def swamee_jain_f(Re, e, D):
    # Swamee-Jain explicit approximation (valid for turbulent flow)
    if Re <= 0:
        return None
    if Re < 2300:
        # laminar flow
        return 64.0 / Re
    # avoid zero or negative inside log
    try:
        f = 0.25 / (math.log10((e/(3.7*D)) + (5.74/(Re**0.9)))**2)
        return f
    except Exception:
        return None


def colebrook_iterative(Re, e, D, init_f=0.02, niter=40):
    if Re <= 0:
        return None
    if Re < 2300:
        return 64.0 / Re
    f = init_f
    for _ in range(niter):
        # avoid domain error
        try:
            denom = (e/(3.7*D)) + (2.51/(Re*math.sqrt(f)))
            val = -2.0*math.log10(denom)
            f_new = 1.0/(val**2)
            if abs(f_new - f) < 1e-6:
                return f_new
            f = f_new
        except Exception:
            break
    return f


# -----------------------------
# HIDRÁULICA: cálculos por tramo
# -----------------------------

def compute_tramo(L, D_m, Q_m3s, e, mu=1e-3, rho=1000.0, method='colebrook'):
    # retorna dict con resultados
    A = math.pi*(D_m**2)/4.0
    if A <= 0:
        raise ValueError("Diámetro inválido")
    V = Q_m3s / A
    Re = rho*V*D_m / mu
    if method == 'swamee':
        f = swamee_jain_f(Re, e, D_m)
    else:
        f = colebrook_iterative(Re, e, D_m)
    if f is None or f <= 0:
        raise ValueError("No se pudo calcular el factor de fricción")
    g = 9.81
    hf = f*(L/D_m)*(V**2/(2*g))
    return {
        'L': L,
        'D_m': D_m,
        'Q_m3s': Q_m3s,
        'A': A,
        'V': V,
        'Re': Re,
        'f': f,
        'hf': hf
    }


# -----------------------------
# EXPORT / IMPORT
# -----------------------------

def export_results_csv(path, profile_z, tramos_results, total_h, names=None):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['estacion_idx', 'elevacion(m)'])
        for i, z in enumerate(profile_z):
            w.writerow([i+1, f"{z:.4f}"])
        w.writerow([])
        w.writerow(['tramo', 'L(m)', 'D(m)', 'Q(m3/s)', 'V(m/s)', 'Re', 'f', 'hf(m)'])
        for i, t in enumerate(tramos_results):
            w.writerow([i+1, f"{t['L']:.4f}", f"{t['D_m']:.4f}", f"{t['Q_m3s']:.6f}",
                        f"{t['V']:.4f}", f"{t['Re']:.0f}", f"{t['f']:.6f}", f"{t['hf']:.6f}"])
        w.writerow([])
        w.writerow(['total_head_loss(m)', f"{total_h:.6f}"])


# -----------------------------
# INTERFAZ (Tkinter)
# -----------------------------

def run_gui():
    root = tk.Tk()
    root.title('Flujo hidráulico + Topografía')
    root.geometry('1000x700')

    # frames
    left = tk.Frame(root)
    left.pack(side='left', fill='both', expand=True, padx=8, pady=8)
    right = tk.Frame(root)
    right.pack(side='right', fill='y', padx=8, pady=8)

    # LEFT: Topografía input
    tk.Label(left, text='Matriz de elevaciones (filas → líneas, separador espacio o coma)', font=('Segoe UI', 10, 'bold')).pack(anchor='w')
    txt_matrix = tk.Text(left, width=60, height=12)
    txt_matrix.pack()

    # example buttons
    ex_frame = tk.Frame(left)
    ex_frame.pack(fill='x', pady=4)
    def load_example_flat():
        example = '\n'.join(['12.00 12.00 12.00 12.00']*4)
        txt_matrix.delete('1.0', tk.END)
        txt_matrix.insert(tk.END, example)
    def load_example_slope():
        example = '\n'.join(['10.0 11.0 12.0 13.0']*4)
        txt_matrix.delete('1.0', tk.END)
        txt_matrix.insert(tk.END, example)
    tk.Button(ex_frame, text='Ejemplo plano', command=load_example_flat).pack(side='left', padx=4)
    tk.Button(ex_frame, text='Ejemplo pendiente', command=load_example_slope).pack(side='left', padx=4)

    # profile extraction
    prof_frame = tk.Frame(left)
    prof_frame.pack(fill='x', pady=6)
    tk.Label(prof_frame, text='Extraer perfil de (fila o columna, 0-index):').pack(side='left')
    spin_rc = tk.StringVar(value='fila')
    ttk.Combobox(prof_frame, values=['fila', 'columna'], textvariable=spin_rc, width=8).pack(side='left', padx=4)
    ent_index = tk.Entry(prof_frame, width=4)
    ent_index.pack(side='left')
    def extract_profile():
        try:
            mat = parse_matrix_text(txt_matrix.get('1.0', tk.END))
            idx = int(ent_index.get()) if ent_index.get().strip()!='' else 0
            if spin_rc.get() == 'fila':
                if idx <0 or idx>=mat.shape[0]: raise IndexError('Índice fila fuera de rango')
                prof = mat[idx,:].tolist()
            else:
                if idx <0 or idx>=mat.shape[1]: raise IndexError('Índice columna fuera de rango')
                prof = mat[:,idx].tolist()
            # show profile in listbox
            list_profile.delete(0, tk.END)
            for i,z in enumerate(prof):
                list_profile.insert(tk.END, f"{i+1}: {z:.3f}")
            messagebox.showinfo('Perfil', 'Perfil extraído correctamente')
        except Exception as e:
            messagebox.showerror('Error', str(e))
    tk.Button(prof_frame, text='Extraer perfil', command=extract_profile).pack(side='left', padx=6)

    # profile display
    tk.Label(left, text='Perfil longitudinal (editable):', font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(8,0))
    list_profile = tk.Listbox(left, width=40, height=6)
    list_profile.pack()

    prof_ops = tk.Frame(left)
    prof_ops.pack(fill='x')
    def add_wp():
        val = simple_input('Agregar cota', 'Ingrese cota (m)')
        try:
            z = float(val)
            list_profile.insert(tk.END, f"{list_profile.size()+1}: {z:.3f}")
        except Exception:
            messagebox.showerror('Error','Valor inválido')
    def remove_wp():
        sel = list_profile.curselection()
        if sel:
            list_profile.delete(sel[0])
        else:
            messagebox.showwarning('Atención','Seleccione un punto para eliminar')
    tk.Button(prof_ops, text='Agregar cota', command=add_wp).pack(side='left', padx=4, pady=4)
    tk.Button(prof_ops, text='Eliminar cota', command=remove_wp).pack(side='left', padx=4)

    # RIGHT: Tramos y control
    tk.Label(right, text='Lista de tramos (cada fila = 1 tramo)', font=('Segoe UI', 10, 'bold')).pack()
    cols = ('L(m)','D(mm)','Q(L/s)','Material')
    tree = ttk.Treeview(right, columns=cols, show='headings', height=8)
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=80, anchor='center')
    tree.pack()

    tramo_frame = tk.Frame(right)
    tramo_frame.pack(pady=6)
    tk.Label(tramo_frame, text='L(m)').grid(row=0,column=0)
    eL = tk.Entry(tramo_frame, width=6); eL.grid(row=1,column=0)
    tk.Label(tramo_frame, text='D(mm)').grid(row=0,column=1)
    eD = tk.Entry(tramo_frame, width=6); eD.grid(row=1,column=1)
    tk.Label(tramo_frame, text='Q(L/s)').grid(row=0,column=2)
    eQ = tk.Entry(tramo_frame, width=6); eQ.grid(row=1,column=2)
    tk.Label(tramo_frame, text='Mat').grid(row=0,column=3)
    mat_var = tk.StringVar(value='PVC')
    ttk.Combobox(tramo_frame, values=['PVC','PEAD','Fierro galvanizado','Concreto'], textvariable=mat_var, width=12).grid(row=1,column=3)

    def add_tramo():
        try:
            L = float(eL.get())
            Dmm = float(eD.get())
            Qls = float(eQ.get())
            mat = mat_var.get()
            tree.insert('', tk.END, values=(f"{L:.2f}", f"{Dmm:.1f}", f"{Qls:.3f}", mat))
            eL.delete(0,tk.END); eD.delete(0,tk.END); eQ.delete(0,tk.END)
        except Exception:
            messagebox.showerror('Error','Verifique los datos del tramo')
    def remove_tramo():
        sel = tree.selection()
        for s in sel:
            tree.delete(s)
    tk.Button(right, text='Agregar tramo', command=add_tramo).pack(pady=4)
    tk.Button(right, text='Eliminar tramo', command=remove_tramo).pack()

    # options: method and area per station
    opt_frame = tk.Frame(right)
    opt_frame.pack(pady=10)
    tk.Label(opt_frame, text='Método f:').grid(row=0,column=0)
    method_var = tk.StringVar(value='colebrook')
    ttk.Combobox(opt_frame, values=['colebrook','swamee'], textvariable=method_var, width=10).grid(row=0,column=1)

    # compute & visualize
    def compute_all():
        try:
            # read profile
            if list_profile.size() == 0:
                raise ValueError('No hay perfil definido')
            profile_z = []
            for i in range(list_profile.size()):
                text = list_profile.get(i)
                # format "idx: val"
                parts = text.split(':')
                z = float(parts[1].strip())
                profile_z.append(z)
            # read tramos
            items = tree.get_children()
            if not items:
                raise ValueError('No hay tramos definidos')
            tramos = []
            rug_map = {'PVC':1.5e-6,'PEAD':7e-6,'Fierro galvanizado':1.5e-4,'Concreto':3e-4}
            tramos_results = []
            total_h = 0.0
            for it in items:
                L = float(tree.item(it,'values')[0])
                Dmm = float(tree.item(it,'values')[1])
                Qls = float(tree.item(it,'values')[2])
                mat = tree.item(it,'values')[3]
                Dm = Dmm/1000.0
                Qm3s = Qls/1000.0
                e = rug_map.get(mat, 1.5e-6)
                res = compute_tramo(L, Dm, Qm3s, e, method=method_var.get())
                tramos_results.append(res)
                total_h += res['hf']
            # account elevation differences along profile as additional head change (optional)
            # For reporting, compute net elevation change
            delta_z = profile_z[-1] - profile_z[0] if len(profile_z)>1 else 0.0
            # show results
            report = f"Total pérdida por fricción (suma tramos) = {total_h:.3f} m\n"
            report += f"Cambio neto de elevación entre inicio y fin = {delta_z:.3f} m\n"
            report += "\nTramos (hf m):\n"
            for i,r in enumerate(tramos_results):
                report += f"Tramo {i+1}: L={r['L']} m, D={r['D_m']:.3f} m, Q={r['Q_m3s']:.4f} m3/s, V={r['V']:.3f} m/s, hf={r['hf']:.4f} m\n"
            messagebox.showinfo('Resultados', report)
            # plots
            fig1, ax1 = plt.subplots()
            # heatmap if matrix exists
            try:
                mat = parse_matrix_text(txt_matrix.get('1.0', tk.END))
                im = ax1.imshow(mat, cmap=cm.terrain)
                ax1.set_title('Mapa de elevaciones')
                plt.colorbar(im, ax=ax1, label='m')
            except Exception:
                ax1.text(0.5,0.5,'No hay matriz válida',ha='center')
            # profile plot
            fig2, ax2 = plt.subplots()
            stations = list(range(1, len(profile_z)+1))
            ax2.plot(stations, profile_z, marker='o')
            ax2.set_xlabel('Estación')
            ax2.set_ylabel('Elevación (m)')
            ax2.set_title('Perfil longitudinal')
            plt.show()
            # offer export
            if messagebox.askyesno('Exportar', '¿Desea exportar resultados CSV?'):
                p = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files','*.csv')])
                if p:
                    export_results_csv(p, profile_z, tramos_results, total_h)
                    messagebox.showinfo('Exportado', f'Archivo exportado: {p}')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    tk.Button(right, text='Calcular y visualizar', command=compute_all, bg='orange').pack(pady=8)

    def simple_input(title, prompt):
        win = tk.Toplevel(root)
        win.title(title)
        tk.Label(win, text=prompt).pack(padx=8,pady=8)
        ent = tk.Entry(win)
        ent.pack(padx=8,pady=4)
        val = {'res':None}
        def ok():
            val['res'] = ent.get()
            win.destroy()
        tk.Button(win, text='OK', command=ok).pack(pady=6)
        root.wait_window(win)
        return val['res']

    # menu
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    def load_csv_matrix():
        p = filedialog.askopenfilename(filetypes=[('CSV files','*.csv')])
        if not p: return
        with open(p,'r',encoding='utf-8-sig') as f:
            txt = f.read()
        txt_matrix.delete('1.0', tk.END)
        txt_matrix.insert(tk.END, txt)
    def save_profile():
        if list_profile.size()==0:
            messagebox.showwarning('Atención','No hay perfil para guardar')
            return
        p = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files','*.csv')])
        if p:
            with open(p,'w',newline='',encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(['estacion','elevacion(m)'])
                for i in range(list_profile.size()):
                    parts = list_profile.get(i).split(':')
                    z = float(parts[1].strip())
                    w.writerow([i+1,f"{z:.4f}"])
            messagebox.showinfo('Guardado', f'Perfil guardado en {p}')
    file_menu.add_command(label='Cargar matriz (CSV)', command=load_csv_matrix)
    file_menu.add_command(label='Guardar perfil (CSV)', command=save_profile)
    menubar.add_cascade(label='Archivo', menu=file_menu)
    root.config(menu=menubar)

    root.mainloop()


if __name__ == '__main__':
    run_gui()
