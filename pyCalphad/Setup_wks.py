from pycalphad import Workspace, Database, variables as v
import pandas as pd
import numpy as np

# -----------------------------------------------------------------------------------------------
# TDB CONDIÇÕES

db = Database('mc_fe_v2062.tdb')
comps = ['FE', 'C','AL','MN','SI', 'VA']
phases = list(db.phases.keys())
condit = {v.X('C'): 0.001,
          v.X('AL'):0.02,
          v.X('MN'):0.1,
          v.X('SI'):0.005,
          v.T: 600,
          v.P: 101325}

# -----------------------------------------------------------------------------------------------

wks = Workspace(db, comps, phases, condit)

# INTERVALO DE TEMPERATURA E QUANTIDADE MOLAR

var_temp = np.arange(500, 1800, 1)
dados = []

# -----------------------------------------------------------------------------------------------

# ITERAÇÃO PARA VARIAÇÃO DE TEMPERATURA <<<<<<<<<<<<<<<<<<<<<< ALTERAR ELEMENTO NO LOOP

for t in var_temp:
        wks.conditions[v.T] = t

# ITERANDO PARA AS FASES PRESENTES NA CONDIÇÃO ATUAL

        fases_eq = wks.eq.Phase.flatten()
        fracoes_eq = wks.eq.NP.flatten()
        
        fases_ativas = {str(f): round(float(nf), 3)
                for f, nf in zip(fases_eq, fracoes_eq)
                if f != ''}

        dados.append({
            'Temperature_K': t,
            'Gibbs_Mol': float(wks.get('GM')),
            'Enthalpy_Mol': float(wks.get('HM')),
            'Heat_Cap_Mol': float(wks.get('CPM')),
            'Phases': '+'.join(sorted(set(fases_ativas))),
            'Phase_Fractions': fases_ativas
        })
        
df = pd.DataFrame(dados)

df_fractions = pd.json_normalize(df['Phase_Fractions']).fillna(0)
df = pd.concat([df.drop(columns='Phase_Fractions'), df_fractions], axis=1)

# -----------------------------------------------------------------------------------------------
