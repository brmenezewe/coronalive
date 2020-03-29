import datetime
import os
import tkinter as tk
import tkinter.ttk as ttk
import pandas
from pandas import DataFrame
import z_common

pandas.set_option("display.max_rows", None, "display.max_columns", None)

class MainWindow(tk.Tk):
    def __init__(self, title=''):
        tk.Tk.__init__(self, title)
        tk.Tk.wm_title(self, title)
        self.configure(background='#222222')

        HEX_cases = '#E60000'
        HEX_deaths = '#a600ff'
        HEX_serious = '#ff4d00'
        HEX_rec = '#70A800'

        self.total_cases = format(data_glb['total_cases'], ',d').replace(',', '.')
        total_deaths = format(data_glb['total_deaths'], ',d').replace(',', '.')
        total_recovered = format(data_glb['total_recovered'], ',d').replace(',', '.')

        css = ttk.Style()
        css.configure('TFrame', background='#222222')
        css.configure('Lfig.TFrame', background='#222222', relief='solid')
        css.configure('Md.Label', background='#222222', foreground='white', font=('Calibri', 20, 'bold'))
        css.configure('Lfig.Label', background='#222222', foreground='white', font=('Calibri', 42, 'bold'))
        css.configure('TLabel', background='#222222', foreground='white', font=('Calibri', 13))
        css.configure('Small_Figure.Label', background='#222222', font=('Calibri', 15, 'bold'))

        # HEADER
        self.f0_head = ttk.Frame(self)
        self.f1_gcases = ttk.Frame(self.f0_head, style='Lfig.TFrame')
        self.f2_gdeaths = ttk.Frame(self.f0_head, style='Lfig.TFrame')
        self.f3_grec = ttk.Frame(self.f0_head, style='Lfig.TFrame')
        self.f4_scope = ttk.Frame(self, style='Lfig.TFrame')
        self.f5_chart = ttk.Frame(self)

        self.lbl1 = ttk.Label(self.f1_gcases, style='Md.Label', text='Total Number of Cases')
        self.lbl2 = ttk.Label(self.f2_gdeaths, style='Md.Label', text='Total Number of Deaths')
        self.lbl3 = ttk.Label(self.f3_grec, style='Md.Label', text='Total Number of Recoveries', foreground='')

        self.lbl_gcases = ttk.Label(self.f1_gcases, style='Lfig.Label', text=self.total_cases, foreground=HEX_cases)
        self.lbl_gdeaths = ttk.Label(self.f2_gdeaths, style='Lfig.Label', text=total_deaths, foreground=HEX_deaths)
        self.lbl_grec = ttk.Label(self.f3_grec, style='Lfig.Label', text=total_recovered, foreground=HEX_rec)

        # BODY
        self.frames = []
        self.labels = {}
        j = 0
        scope = {'BR', 'EG', 'CN', 'GH', 'UA', 'CH', 'PT', 'PH', 'IN', 'US'}
        for k, country in enumerate(data_glb_li):
            if country != 'stat':
                d = data_glb_li[str(k + 1)]
                if d['code'] in scope:
                    death_ratio = str(d['total_deaths'] / d['total_cases'] * 100)[:3]
                    self.frames.append(ttk.Frame(self.f4_scope))
                    self.labels.update({'c1r' + str(j): ttk.Label(self.frames[j], text=d['title'], width=11)})
                    self.labels.update({'c2r' + str(j): ttk.Label(self.frames[j], text=format(d['total_cases'], ',d').replace(',', '.'), style='Small_Figure.Label', foreground=HEX_cases, width=7)})
                    self.labels.update({'c3r' + str(j): ttk.Label(self.frames[j], text='(+' + str(d['total_new_cases_today']) + ' today)', foreground=HEX_cases, width=15)})
                    self.labels.update({'c4r' + str(j): ttk.Label(self.frames[j], text=format(d['total_deaths'], ',d').replace(',', '.'), style='Small_Figure.Label', foreground=HEX_deaths, width=6)})
                    self.labels.update({'c5r' + str(j): ttk.Label(self.frames[j], text='(+' + str(d['total_new_deaths_today']) + ' today)', foreground=HEX_deaths, width=10)})
                    self.labels.update({'c6r' + str(j): ttk.Label(self.frames[j], text= f"{death_ratio}%", foreground=HEX_deaths, width=10)})
                    self.labels.update({'c7r' + str(j): ttk.Label(self.frames[j], text=d['total_serious_cases'], style='Small_Figure.Label', foreground=HEX_serious, width=6)})
                    self.labels.update({'c8r' + str(j): ttk.Label(self.frames[j], text='serious cases', foreground=HEX_serious, width=15)})
                    self.labels.update({'c9r' + str(j): ttk.Label(self.frames[j], text=format(d['total_recovered'], ',d').replace(',', '.'), style='Small_Figure.Label', foreground=HEX_rec, width=6)})
                    self.labels.update({'c10r' + str(j): ttk.Label(self.frames[j], text='recovered', foreground=HEX_rec, width=14)})

                    self.frames[j].pack(anchor='w', padx=15, pady=(2, 2))
                    for l in self.frames[j].winfo_children():
                        l.pack(side='left', padx=(5, 0))

                    j = j + 1

    def add_widgets(self):
        self.f0_head.pack(padx=15, pady=(15, 0))
        self.f1_gcases.pack(side='left')
        self.f2_gdeaths.pack(side='left', padx=50)
        self.f3_grec.pack(side='left')
        self.f4_scope.pack(padx=15, pady=(10, 0))
        self.f5_chart.pack(fill='x', padx=15, pady=10)

        self.lbl1.pack(padx=15, pady=(5, 0))
        self.lbl2.pack(padx=15, pady=(5, 0))
        self.lbl3.pack(padx=15, pady=(5, 0))

        self.lbl_gcases.pack(padx=15, pady=(0, 5))
        self.lbl_gdeaths.pack(padx=15, pady=(0, 5))
        self.lbl_grec.pack(padx=15, pady=(0, 5))

    def add_linechart(self):

        df = pandas.DataFrame.from_records(data_glb_tl)
        df['cases'] = df['cases'].astype(int)
        df['deaths'] = df['deaths'].astype(int)
        df['recovered'] = df['recovered'].astype(int)
        df = df.groupby('date')[['cases', 'deaths']].sum().reset_index()
        #now = datetime.datetime.now()
        #timeline_d.update({now.strftime('%m/%d/%y') : int(self.total_cases.replace('.', ''))})

        z_common.chart_add(self.f5_chart, df)

if __name__ == '__main__':
    rsc = os.path.join(z_common.app_path(), 'rsc')

    url_glb = 'https://thevirustracker.com/free-api?global=stats'
    url_glb_li = 'https://thevirustracker.com/free-api?countryTotals=ALL'
    url_glb_tl = 'https://thevirustracker.com/timeline/map-data.json'

    data_glb = z_common.json_call_api(url_glb)
    data_glb = data_glb['results'][0]

    data_glb_li = z_common.json_call_api(url_glb_li)
    data_glb_li = data_glb_li['countryitems'][0]

    data_glb_tl = z_common.json_call_api(url_glb_tl)
    data_glb_tl = data_glb_tl['data']

    z_common.write_json(os.path.join(rsc, 'data_glb.json'), data_glb)
    z_common.write_json(os.path.join(rsc, 'data_glb_li.json'), data_glb_li)
    z_common.write_json(os.path.join(rsc, 'data_glb_tl.json'), data_glb_tl)

    # __ini__ UI
    root = MainWindow('COVID-19 Live Updates by W*M')
    root.add_widgets()
    root.add_linechart()
    z_common.form_center(root)
    root.mainloop()