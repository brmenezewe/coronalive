#################
### Version 1.1 #
#################
import datetime, json, locale, os, sys
import requests
from PyQt5.QtWidgets import *


# -=-=-=-=-=-=-=-= Date & Time =-=-=-=-=-=-=-=-#


def timestamp():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d%H%M%S')

def str_to_date(strdate, input_format, output_format):
    return datetime.datetime.strptime(strdate, input_format).strftime(output_format)

# -=-=-=-=-=-=-=-= Data Visualization =-=-=-=-=-=-=-=-#

def chart_add(frame, df):

    import matplotlib.pyplot as pyplot
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    HEX_light_gray = '#343434'

    figure = pyplot.Figure(figsize=(8, 5), dpi=100)
    ax = figure.add_subplot(111, facecolor='#222222')

    line = FigureCanvasTkAgg(figure, frame)
    line.get_tk_widget().pack(fill='both')

    df.plot(kind='line', legend=True, x='date', y='cases', ax=ax, color='r', marker='o', fontsize=10)
    df.plot(kind='line', legend=True, x='date', y='deaths', ax=ax, secondary_y=True, color='purple', marker='x', fontsize=10)

    figure.tight_layout()
    figure.set_facecolor('#222222')
    ax.grid(True, linestyle="--", color=HEX_light_gray)
    ax.tick_params(colors='white')
    ax.right_ax.tick_params(colors='white')
    ax.set_xlabel('', color='white')

    sides = ['left', 'right', 'top', 'bottom']
    for s in sides:
        ax.spines[s].set_color(HEX_light_gray)
        ax.right_ax.spines[s].set_color(HEX_light_gray)
        if s == 'right' or s =='top':
            ax.spines[s].set_linestyle('--')
            ax.right_ax.spines[s].set_linestyle('--')

    ax.set_yticklabels(['{:,}'.format(int(x)).replace(',', '.') for x in ax.get_yticks().tolist()])
    ax.right_ax.set_yticklabels(['{:,}'.format(int(x)).replace(',', '.') for x in ax.right_ax.get_yticks().tolist()])

#-=-=-=-=-=-=-=-= File Explorer =-=-=-=-=-=-=-=-#


def app_path():
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return application_path


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def filecount(directory, subdir = False):
    return len([filename for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))])



#-=-=-=-=-=-=-=-= Parse =-=-=-=-=-=-=-=-#

def json_call_api(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    resp = requests.get(url=url, headers=headers)
    return resp.json()


def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent = 4)


def curr_to_dec(strcurr):
    locale.setlocale(locale.LC_ALL, 'pt_br')
    strcurr = strcurr.replace('R$', '')
    return locale.atof(strcurr)


#-=-=-=-=-=-=-=-= Validation =-=-=-=-=-=-=-=-#


def validate_extension(extension, tuple_of_extensions, debug_print = False):
    if extension.find('\\') > 0 or extension.find('/') > 0:
        extension = os.path.splitext(extension)[1]
    extension = extension.lower().replace('.','')
    if debug_print:
        import inspect
        print('Function "{0}" - - - Input extension: {1} - - - To be found on: {2}'.format(inspect.stack()[0][3], extension, tuple_of_extensions))
    for i in tuple_of_extensions:
        if i[1][2:].lower() == extension:
            return True
        else:
            return False


#-=-=-=-=-=-=-=-= Others =-=-=-=-=-=-=-=-#


def form_center(form):
    form.update_idletasks()
    sw = form.winfo_screenwidth()
    sh = form.winfo_screenheight()
    x = (sw / 2) - (form.winfo_width() / 2)
    y = (sh / 2) - (form.winfo_height() / 2)
    form.geometry('%dx%d+%d+%d' % (form.winfo_width(), form.winfo_height(), x, y))

def qt_form_center(form):
    qr = form.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    form.move(qr.topLeft())

# TESTING
if __name__ == '__main__':
    print(str_to_date('1/30/20', '%m/%d/%y', '%b %d %y'))