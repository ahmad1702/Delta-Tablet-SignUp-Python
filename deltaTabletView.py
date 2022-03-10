import PySimpleGUI as sg
import pandas as pd
import os
import os.path

sg.theme('DarkTeal9')

deletes = False

#Airplane Seat List
realseatlist = ['29F', '21C', '21A']
class AirplaneSeatList():
    def __init__(self,seatlist):
        self.seatlist = seatlist
    
    seatlist = ['29F', '21C', '21A']


# Layout Design
layout = [
    [sg.Text('Welcome to Delta Business Solutions!', font=('Any 45'))],
    [sg.Text('Please fill out the following fields:', font=('Any 24'))],
    [sg.Text('ID Number', size=(11,1), font=('Any 24')), sg.InputText(key='Section Number', font=('Any 24'))],
    [sg.Text('Section number', size=(11,1), font=('Any 24')), sg.InputText(key='Airplane Seat', font=('Any 24'))],
    [sg.Text('First Name', size=(11,1), font=('Any 24')), sg.InputText(key='First Name', font=('Any 24'))],
    [sg.Text('Last Name', size=(11,1), font=('Any 24')), sg.InputText(key='Last Name', font=('Any 24'))],
    [sg.Text('E-Mail', size=(11,1), font=('Any 24')), sg.InputText(key='E-Mail', font=('Any 24'))],
    [sg.Text('Password', size=(11,1), font=('Any 24')), sg.InputText(key='Password', font=('Any 24'))],
    [sg.Text('Phone Number', size=(11,1), font=('Any 24')), sg.InputText(key='Phone Number', font=('Any 24'))],
    [sg.Text('Covid Status', size=(11,1), font=('Any 24')), 
                        sg.Checkbox('Positive Confirmed Test', key='Positive', font=('Any 24')),
                        sg.Checkbox('Negative Confirmed Test', key='Negative', font=('Any 24')),
                        sg.Checkbox('Not Tested', key='Not Tested', font=('Any 24'))],
    [sg.Text('Preferred Methods of Contact', size=(22,1), font=('Any 24')), 
                        sg.Checkbox('SMS Text', key='prefSMS', font=('Any 24')),
                        sg.Checkbox('Phone Call', key='prefPhone', font=('Any 24')),
                        sg.Checkbox('E-Mail', key='prefMail', font=('Any 24'))],
    [sg.Submit(), sg.Button('Clear'), sg.Button('Delete Account'), sg.Exit()]
]

window = sg.Window('Delta Business Solutions Portal', layout)

def clear_input():
    for key in values:
        window[key]('')
    return None

while True:
    event, values = window.read()
    if event ==  sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        clear_input()
    if event == 'Submit':
        userSection = values['Section Number']
        EXCEL_FILE = userSection + '.xlsx'
        file_exists = os.path.isfile(EXCEL_FILE)

        if file_exists:
            df = pd.read_excel(EXCEL_FILE)

            df = df.append(values, ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)
        else:
            writer = pd.ExcelWriter(EXCEL_FILE, engine='xlsxwriter')
            writer.save()
            df = pd.read_excel(EXCEL_FILE)

            df = df.append(values, ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)
        
        sg.popup('Thank You for Choosing Delta Business Solutions, Have a Good Day!')
        clear_input()
        break
    if event == 'Delete Account':
        deletes = True
        break
window.close()

if deletes == True:
    layout2 = [
    [sg.Text('Account Deletion', font=('Any 30'))],
    [sg.Text('Please fill out the following fields:', font=('Any 24'))],
    [sg.Text('Section Number', size=(11,1), font=('Any 24')), sg.InputText(key='Section Number2', font=('Any 24'))],
    [sg.Text('E-Mail', size=(11,1), font=('Any 24')), sg.InputText(key='E-Mail2', font=('Any 24'))],
    [sg.Text('Password', size=(11,1), font=('Any 24')), sg.InputText(key='Password2', font=('Any 24'))],
    [sg.Submit(), sg.Exit()]
    ]
    window2 = sg.Window('Simple data entry form', layout2)

    def clear_input():
        for key in values:
            window2[key]('')
        return None

    while True:
        event, values = window2.read()
        if event ==  sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Clear':
            clear_input()
        if event == 'Submit':
            currentemail = values['E-Mail2']
            currpass = values['Password2']

            excelFile = values['Section Number2'] + '.xlsx'
            df = pd.read_excel(excelFile)

            deletelist = []
         
            column = df['Section Number']
            max_value = column.max()
            for i in range(1,max_value):
                if df.iloc[i]['E-Mail'] == currentemail and df.iloc[i]['Password'] == df.iloc[i]['Password2']:
                    deletelist.append(i)
        
            data = df.drop(labels=deletelist, axis=0)

            os.remove(excelFile)

            writer = pd.ExcelWriter(excelFile, engine='xlsxwriter')
            writer.save()

            element1 = values.pop('Section Number2')
            element2 = values.pop('E-Mail2')
            element3 = values.pop('Password2')

            data = data.append(values, ignore_index=True)
            data.to_excel(excelFile, index=False)

            break

    window2.close()