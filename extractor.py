# CELL 0

from selenium import webdriver
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import pandas as pd

# CELL 1

# Creates the dataframe where it will save the extracted data

df = pd.DataFrame(columns=['nombre', 'tipo_y_estado', 'informacion_y_municipio', 'nombre_fiscal_comercial', 'ventas', 'circulacion_pagada', 'periodo', 'tiraje', 'ediciones_evaluadas', 'promedio_circulacion', 'directorio'] )

# CELL 2

# Load the driver y and the webpage with Selenium

driver = webdriver.Firefox()
driver.get("https://pnmi.segob.gob.mx/reporte")

driver.maximize_window()
time.sleep(1)

# The program starts. Here it looks for an option in the dropdown menu.
# Tipo indicates the kind of publication. In this case it selects "PERIODICO" (newspapers), you can change it as you need.

dropdown = driver.find_element(By.NAME, "tipo")
dropdown.click()
time.sleep(1)

tipo = Select(dropdown)
tipo.select_by_value('PERIODICO')
time.sleep(1)

diario = driver.find_element(By.XPATH, '//div[@class="col-md-6"][2]//div[@class="form-group"][2]//div[@class="radio"]//div[@class="col-md-4 "][6]//label')
diario.click()
time.sleep(1)

# Clicks on the submit button

submit = driver.find_element(By.XPATH, '//button[@class="btn btn-primary"]')
try:
    submit.click()
    time.sleep(1)
except:
    pass

# Iterates under the media list in the website and extracts the information about sells and circulation of each media

for i in range(0,300) : # the range controls the amount of media over which it iterates. 
  
  # If the program fail change the first number to the corresponding one, which is the next one from where it left, and start the CELL 2 again.
    
    try: 
        time.sleep(5)
      
        # In each iteration, recharges the elements of the DOM
        medios = driver.find_elements(By.XPATH, '//div[@class="col-md-10 resultado redireccion"]')

        # Saves the media name in its correspondent variable
        nombre_del_medio = medios[i].text

        medios[i].click()
        time.sleep(1)
        
        # Extracts information from the section "información inicial"
        
        informacion_inicial = driver.find_elements(By.XPATH, '//div[@id="informacion-inicial"]//div[@class="row"]//div[@class="col-md-4"]')
        tipo_y_estado = informacion_inicial[0].text  
        informacion_y_municipio = informacion_inicial[1].text
        print(tipo_y_estado)
        print(informacion_y_municipio)
        
       
        # Extracts information from the section "Información sobre el medio impreso"
      
        informacion_medio_impreso = driver.find_element(By.XPATH, '//ul[@class="nav nav-tabs nav-justified navfont"]/li[2]')
        informacion_medio_impreso.click()
        time.sleep(1)
        
        informacion_medio = driver.find_elements(By.XPATH, '//div[@id="informacion-sobre-el-medio-impreso"]//div[@class="col-md-12"]')
        nombre_fiscal_comercial = informacion_medio[0].text
        print(nombre_fiscal_comercial)
        
        info_directorio = driver.find_elements(By.XPATH, '//div[@id="informacion-sobre-el-medio-impreso"]//div[@class="row"][7]')
        directorio = info_directorio[0].text

        # Search and save in variables the sells and circulation data for each media

        circulacion = driver.find_element(By.XPATH, '//ul[@class="nav nav-tabs nav-justified navfont"]/li[4]')
        circulacion.click()
        time.sleep(1)
         
        ventas = driver.find_elements(By.XPATH, '//div[@id="circulacion-y-distribucion-geografica"]/div["row"]/div["col-md-5"][1]')
        ventas = ventas[3].text
        print(ventas)
        circulacion_pagada = driver.find_element(By.XPATH, '//div[@id="circulacion-y-distribucion-geografica"]/div["row"]/div["col-md-5"][2]')
        circulacion_pagada = circulacion_pagada.text
        print(circulacion_pagada)

        periodo = driver.find_element(By.XPATH, '//div[@id="circulacion-y-distribucion-geografica"]//div[@class="row"][1]//div[@class="col-md-12"]//p[3]')
        periodo = periodo.text
        print(periodo)
        
        tiraje = driver.find_element(By.XPATH, '//div[@id="circulacion-y-distribucion-geografica"]//div[@class="row"][2]//div[@class="col-md-12"]//p[1]')
        tiraje = tiraje.text
        print(tiraje)
        
        ediciones_evaluadas = driver.find_element(By.XPATH, '//div[@id="circulacion-y-distribucion-geografica"]//div[@class="row"][3]//div[@class="col-md-12"]//p[1]')
        ediciones_evaluadas = ediciones_evaluadas.text
        print(ediciones_evaluadas)
        
        promedio_circulacion = driver.find_element(By.XPATH, '//div[@id="circulacion-y-distribucion-geografica"]//div[@class="row"][3]//div[@class="col-md-12"]//p[2]')
        promedio_circulacion = promedio_circulacion.text
        
        # 2 steps back, reload the page and accept the alert from Firefox.

        driver.execute_script("window.history.go(-1)")
        time.sleep(1)
        driver.execute_script("window.history.go(-1)")
        time.sleep(1)
        driver.execute_script("window.history.go(-1)")
        time.sleep(1)
        driver.refresh()
        time.sleep(1)
        try:
            Alert(driver).accept()
            time.sleep(1)
        except:
            pass

        # Before another iteration, it saves the data on the dataframe
        
        datos = ({'nombre': nombre_del_medio, 
                      'tipo_y_estado' : tipo_y_estado,
                      'informacion_y_municipio' : informacion_y_municipio,
                      'nombre_fiscal_comercial' : nombre_fiscal_comercial,
                      'periodo': periodo,
                      'tiraje' : tiraje,
                      'ediciones_evaluadas': ediciones_evaluadas,
                      'promedio_circulacion': promedio_circulacion,
                      'ventas': ventas, 
                      'circulacion_pagada': circulacion_pagada,
                      'directorio': directorio})
        datos = pd.Series(datos) 
        df = df.append(datos, ignore_index=True)

        time.sleep(5)
        
    except: 
        print(df)
        break

# CELL 3

# Exports the dataframe to a CSV file when you have all the entries you need.

df.to_csv('base_de_datos.csv', encoding = "utf-8-sig")
