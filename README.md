# ICME: Thermodynamic and Solidification Simulation of High-Mn Alloy
Este repositório apresenta uma metodologia integrada de ICME (Integrated Computational Materials Engineering) para simular a solidificação de uma liga complexa de Manganês. O diferencial é o uso de dados termodinâmicos reais (via CALPHAD) para alimentar as condições de contorno e propriedades físicas no OpenFOAM.

# Etapa 1: Modelagem Termodinâmica (PyCalphad)
Nesta etapa, utilizamos o método CALPHAD para prever o comportamento de fases da liga.
* **Base de Dados:** mc_fe_v2062.tdb
* **Composição Nominal:**
  * **Mn:** 0.1
  * **Al:** 0.02
  * **Si:** 0.005
  * **C:** 0.001
* **Faixa de Temperatura:** 500 K a 1800 K (passo de 1 K).
O script 'Setup_wks.py' extrai propriedades fundamentais que variam com a temperatura, eliminando a necessidade de usar propriedades constantes e simplificadas na simulação:
* **Frações de Fases:** Identificação das janelas de solidificação.
* **Termofísica:** Energia de Gibbs (G), Entalpia (H) e Capacidade Calorífica (Cp).
Os dados termodinâmicos obtidos via PyCalphad são utilizados como entrada no OpenFOAM,
permitindo a definição de propriedades dependentes da temperatura e melhor representação
do processo de solidificação.

# Etapa 2: Simulação de Fluidodinâmica e Solidificação (OpenFOAM)
Com os dados térmicos, utilizou-se o OpenFOAM para modelar o resfriamento da liga em um molde.
* **Solver:** 'chtMultiRegionFoam'
* **Modelagem de solidificação:** 'fvOptions' com 'solidificationSource'
**Condições Iniciais e de Contorno:**
* **Temperatura Inicial do Metal Líquido (T0):** 1800 K.
* **Domínio:** Representação do molde e da liga metálica (pastas 'constant' e 'system').
* **Física Envolvida:** Transferência de calor por condução e convecção, considerando a liberação de calor latente durante a mudança de fase.

# Como executar
Na interface Python (3.10.20) rode 'Setup_wks.py' na mesma pasta que contenha o banco de dados 'mc_fe_v2062.tdb'.
O output gerará dados de $H(T)$, $T_{liquidus}$ e $T_{solidus}$ e Cp médio da fase líquida. Nota: Os valores molares ($/mol$) devem ser convertidos para base mássica ($/kg$) antes da inserção no OpenFOAM.
Usando o OpenFOAM (v2412), maior parte dos dados gerados pela termodinâmica serão usados em constant/liqmetal/thermophysicalProperties ou em system/liqmetal/fvOptions.
Comandos de processo: blockMesh -> checkMesh -> setFields -> chtMultiRegionFoam
A integração final dos resultados podem ser visualizados no ParaView
