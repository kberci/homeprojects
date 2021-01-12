import json
import datetime
import matplotlib.pyplot as plt
import numpy as np

SETTINGS = {
    'full_name1': 'John Smith',
    'full_name2': 'Isabel Smith',
    'nick_name1': 'John',
    'nick_name2': 'Isabel',
}
JSON_PATH = './message_1.json'


def initialize_dict(current_date):
    return {
        'date': current_date,
        SETTINGS['nick_name1']: {
            'questions': 0,
            'msg_len': 0,
            'num_msg': 0
        },
        SETTINGS['nick_name2']: {
            'questions': 0,
            'msg_len': 0,
            'num_msg': 0}}


def update_values(msg, processed_result):
    sender = SETTINGS['nick_name1'] if SETTINGS['full_name1'] in msg[
        'sender_name'] else SETTINGS['nick_name2']
    processed_result[sender]['questions'] += msg['content'].count('?')
    processed_result[sender]['msg_len'] += len(msg['content']) / 10
    processed_result[sender]['num_msg'] += 1
    return processed_result


def process_results(json_name):
    f = open(json_name)
    doc = json.load(f)

    processed_all, prev_date = [], None
    processed = initialize_dict(None)

    for m in doc['messages']:
        if "content" in m:
            date = datetime.datetime.fromtimestamp(
                m['timestamp_ms'] / 1000.0).date()
            if prev_date == date:
                update_values(m, processed)
            else:
                if prev_date:
                    processed_all.append(processed)
                processed = initialize_dict(date)
                update_values(m, processed)
                prev_date = date
    processed_all.reverse()
    return processed_all


def plot_results(result_array, output_name=None):
    palette = plt.get_cmap('Set1')
    plot_settings = [
        {'name': 'questions',
         'marker': '.',
         'label': 'Number of questions - '},
        {'name': 'msg_len',
         'marker': '*',
         'label': 'Total msg lengths (char*10) - '},
        {'name': 'num_msg',
         'marker': 's',
         'label': 'Number of msg - '}]

    for method in ['daily', 'cumulative']:
        plt.figure(figsize=(15, 10))
        plt.style.use('seaborn-darkgrid')
        pal = 1
        for name in list(SETTINGS.values())[2:]:
            for setting in plot_settings:
                x = [i['date'] for i in result_array]
                y = [i[name][setting['name']] for i in
                     result_array] if method == 'daily' else np.cumsum(
                    [i[name][setting['name']] for i in result_array])
                plt.plot(x, y, marker=setting['marker'], color=palette(pal),
                         linewidth=1, alpha=0.9, label=setting['label'] + name)
            pal += 3
        plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
        plt.legend(ncol=2)
        plt.title("Messenger-activity " + method + " comparison (" + min(
            [r['date'] for r in result_array]).strftime(
            "%Y/%m/%d") + " - " + max(
            [r['date'] for r in result_array]).strftime("%Y/%m/%d") + ')',
                  size=20)
        plt.xlabel("Date")
        if output_name:
            plt.savefig(output_name + "_" + method)
        else:
            plt.show()
        plt.close()


plot_results(result_array=process_results(JSON_PATH),
             output_name='example')
