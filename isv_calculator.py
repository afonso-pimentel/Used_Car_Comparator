import datetime

def calculateIsv(displacement, emissions, fuel, price, productionYear):
# Defino as variáveis
# preciso mesmo da palavra valor à frente das variáveis?!
# variável da cilindrada do ISV, será boa ideia criar duas variáveis, uma para cada imposto? é que a variável não muda, é sempre a mesma!
    DadosISVcm3 = 0
# variável do CO2
    DadosISVCO2 = 0
# variável do combustível para poder apresentar o feedback na simulação
    DadosCombustivel = ""
# defino como 10% o valor das taxas aduaneiras - é o máximo possível
    TaxasAduaneirasPercentagem = 0.1
# o valor mínimo do ISV é sempre 100€, tenho que definir essa variável, assim como o valor do IVA para o caso dos novos e dos importados fora UE
    ValorISVMinimo = 100
    ValorPercentagemIVA = 1.23
    ValorIVA = 0.23
# preciso do valor do carro para apresentar resultados com o valor incluído, para apresentar um "PVP", para calcular o IVA e as taxas aduaneiras
    ValorCarro = 0
    ValorTaxas = 0
    ValorDespesasImportacao = 0
    SimboloEuro = "€"
    DadosISVCO2WLTP = ""
# defino as variáveis com os descontos da idade cilindrada
    DescontoIdadeAte6Meses = 0.1
    DescontoIdadeMais6Mesesa1Ano = 0.1
    DescontoIdadeMais1a2Anos = 0.2
    DescontoIdadeMais2a3Anos = 0.28
    DescontoIdadeMais3a4Anos = 0.35
    DescontoIdadeMais4a5Anos = 0.43
    DescontoIdadeMais5a6Anos = 0.52
    DescontoIdadeMais6a7Anos = 0.6
    DescontoIdadeMais7a8Anos = 0.65
    DescontoIdadeMais8a9Anos = 0.7
    DescontoIdadeMais9a10Anos = 0.75
    DescontoIdadeMais10a11Anos = 0.8
    DescontoIdadeMais11a12Anos = 0.8
    DescontoIdadeMais12a13Anos = 0.8
    DescontoIdadeMais13a14Anos = 0.8
    DescontoIdadeMais14a15Anos = 0.8
    DescontoIdadeMais15Anos = 0.8

# defino as variáveis com os descontos da idade CO2
    DescontoCO2IdadeAte6Meses = 0.10
    DescontoCO2IdadeMais6Mesesa1Ano = 0.10
    DescontoCO2IdadeMais1a2Anos = 0.10
    DescontoCO2IdadeMais2a3Anos = 0.20
    DescontoCO2IdadeMais3a4Anos = 0.20
    DescontoCO2IdadeMais4a5Anos = 0.28
    DescontoCO2IdadeMais5a6Anos = 0.28
    DescontoCO2IdadeMais6a7Anos = 0.35
    DescontoCO2IdadeMais7a8Anos = 0.43
    DescontoCO2IdadeMais8a9Anos = 0.43
    DescontoCO2IdadeMais9a10Anos = 0.52
    DescontoCO2IdadeMais10a11Anos = 0.60
    DescontoCO2IdadeMais11a12Anos = 0.60
    DescontoCO2IdadeMais12a13Anos = 0.65
    DescontoCO2IdadeMais13a14Anos = 0.70
    DescontoCO2IdadeMais14a15Anos = 0.75
    DescontoCO2IdadeMais15Anos = 0.8
# os benefícios fiscais são dados como x% do valor do ISV, aqui indico as variáveis dos benefícios que não passam de percentagens, daí terem que ser todas 1 inicialmente
    BeneficioHibridoNormalPercentagem = 0.6
    BeneficioHibridoPlugInPercentagem = 0.25
    BeneficioHibrido = 1
# os valores em € das duas componentes
    ValorISVcm3_EsteAno = 0
    ValorISVcm3_ProximoAno = 0
    ValorISVCO2_EsteAno = 0
    ValorISVCO2_ProximoAno = 0
    ValorISVTotal_EsteAno = ValorISVcm3_EsteAno + ValorISVCO2_EsteAno
    ValorISVTotal_ProximoAno = ValorISVcm3_ProximoAno + ValorISVCO2_ProximoAno
    
# Vou buscar os dados aos campos se estiverem preenchidos e atribuo-os às variáveis

# vou buscar a cilindrada ao campo
    if (displacement > 0) :
        DadosISVcm3 = displacement
    
# agora vou buscar o CO2 ao campo
    DadosISVCO2 = emissions
    DadosISVCO2_ProximoAno = emissions
    isHybrid = False
    isPluginHybrid = False
# vejo qual foi o combustível escolhido para definir uma variável para depois dar feedback ao utilizador do combustível que está activo para a simulação
    if fuel == "diesel":
        DadosCombustivel = "Gasoleo"
    elif fuel == "petrol":
        DadosCombustivel = "Gasolina"
    elif fuel == "Hybrid-Petrol":
        isHybrid = True
    elif fuel == "Hybrid-Diesel":
        isHybrid = True
    elif fuel == "Hybrid-Plug-in":
        isPluginHybrid = True
# vou buscar o valor do carro ao campo para apresentar a simulação com o valor do carro incluído, para calcular o valor das taxas aduaneiras a 10% e coloco/retiro os avisos para as importações fora UE
    if (price > 0):
        ValorCarro = price
        ValorTaxas = ValorCarro * TaxasAduaneirasPercentagem

# Cálculos preliminares

# desconto dado aos híbridos
    if (isHybrid):
        BeneficioHibrido = BeneficioHibridoNormalPercentagem
    if (isPluginHybrid):
        BeneficioHibrido = BeneficioHibridoPlugInPercentagem

# vamos calcular a componente cilindrada que é comum ao NEDC e WLTP, coloco a operação lógica porque há pessoas que não preenchem a cilindrada e eu não quero apresentar simulações sem esse dado, o 100 é escolhido por ser um mínimo de 3 algarismos, ao mesmo tempo que preenche o campo, aparece o campo seguinte do CO2, tenho que definir dois anos para poder fazer as comparações entre orçamentos de estado
    if (DadosISVcm3 > 100):
        if (DadosISVcm3 <= 1000):
            ValorISVcm3_EsteAno = (DadosISVcm3 * 1.00) - 777.50
            ValorISVcm3_ProximoAno = (DadosISVcm3 * 1.09) - 849.03
        elif (DadosISVcm3 <= 1250):
            ValorISVcm3_EsteAno = (DadosISVcm3 * 1.08) - 779.02
            ValorISVcm3_ProximoAno = (DadosISVcm3 * 1.18) - 850.69
        elif (DadosISVcm3 > 1250):
            ValorISVcm3_EsteAno = (DadosISVcm3 * 5.13) - 5672.97
            ValorISVcm3_ProximoAno = (DadosISVcm3 * 5.61) - 6194.88
    
# aplico o desconto dos hibridos à componente cilindrada, será boa ideia aplicar este desconto só no fim em vez de o aplicar duas vezes às componentes? Se calhar sim, porque se isto muda para se aplicar o desconto a uma só componente em vez de à totalidade, fico pendurado
    ValorISVcm3_EsteAno = ValorISVcm3_EsteAno * BeneficioHibrido
    ValorISVcm3_ProximoAno = ValorISVcm3_ProximoAno * BeneficioHibrido
# vamos calcular a componente cilindrada com os descontos da idade
    # novo
    ValorISVcm3Novo_EsteAno = ValorISVcm3_EsteAno
    ValorISVcm3Novo_ProximoAno = ValorISVcm3_ProximoAno
    # até 6 meses
    ValorISVcm3Ate6Meses_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeAte6Meses)
    ValorISVcm3Ate6Meses_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeAte6Meses)
    ValorISVTotalAte6Meses_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeAte6Meses)
    # 6 meses a 1 ano
    ValorISVcm3Mais6Mesesa1Ano_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais6Mesesa1Ano)
    ValorISVcm3Mais6Mesesa1Ano_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais6Mesesa1Ano)
    ValorISVTotalMais6Mesesa1Ano_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais6Mesesa1Ano)
    # 1 a 2 anos
    ValorISVcm3Mais1a2Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais1a2Anos)
    ValorISVcm3Mais1a2Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais1a2Anos)
    ValorISVTotalMais1a2Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais1a2Anos)
    # 2 a 3 anos
    ValorISVcm3Mais2a3Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais2a3Anos)
    ValorISVcm3Mais2a3Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais2a3Anos)
    ValorISVTotalMais2a3Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais2a3Anos)
    # 3 a 4 anos
    ValorISVcm3Mais3a4Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais3a4Anos)
    ValorISVcm3Mais3a4Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais3a4Anos)
    ValorISVTotalMais3a4Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais3a4Anos)
    # 4 a 5 anos
    ValorISVcm3Mais4a5Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais4a5Anos)
    ValorISVcm3Mais4a5Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais4a5Anos)
    ValorISVTotalMais4a5Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais4a5Anos)
    # 5 a 6 anos
    ValorISVcm3Mais5a6Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais5a6Anos)
    ValorISVcm3Mais5a6Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais5a6Anos)
    ValorISVTotalMais5a6Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais5a6Anos)
    # 6 a 7 anos
    ValorISVcm3Mais6a7Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais6a7Anos)
    ValorISVcm3Mais6a7Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais6a7Anos)
    ValorISVTotalMais6a7Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais6a7Anos)
    # 7 a 8 anos
    ValorISVcm3Mais7a8Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais7a8Anos)
    ValorISVcm3Mais7a8Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais7a8Anos)
    ValorISVTotalMais7a8Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais7a8Anos)
    # 8 a 9 anos
    ValorISVcm3Mais8a9Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais8a9Anos)
    ValorISVcm3Mais8a9Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais8a9Anos)
    ValorISVTotalMais8a9Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais8a9Anos)
    # 9 a 10 anos
    ValorISVcm3Mais9a10Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais9a10Anos)
    ValorISVcm3Mais9a10Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais9a10Anos)
    ValorISVTotalMais9a10Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais9a10Anos)
    # 10 a 11 anos
    ValorISVcm3Mais10a11Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais10a11Anos)
    ValorISVcm3Mais10a11Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais10a11Anos)
    ValorISVTotalMais10a11Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais10a11Anos)
    # 11 a 12 anos
    ValorISVcm3Mais11a12Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais11a12Anos)
    ValorISVcm3Mais11a12Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais11a12Anos)
    ValorISVTotalMais11a12Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais11a12Anos)
    # 12 a 13 anos
    ValorISVcm3Mais12a13Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais12a13Anos)
    ValorISVcm3Mais12a13Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais12a13Anos)
    ValorISVTotalMais12a13Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais12a13Anos)
    # 13 a 14 anos
    ValorISVcm3Mais13a14Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais13a14Anos)
    ValorISVcm3Mais13a14Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais13a14Anos)
    ValorISVTotalMais13a14Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais13a14Anos)
    # 14 a 15 anos
    ValorISVcm3Mais14a15Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais14a15Anos)
    ValorISVcm3Mais14a15Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais14a15Anos)
    ValorISVTotalMais14a15Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais14a15Anos)
    # mais de 15 anos
    ValorISVcm3Mais15Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais15Anos)
    ValorISVcm3Mais15Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais15Anos)
    ValorISVTotalMais15Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais15Anos)
# definir as variáveis do valor do CO2
    ValorISVCO2Gasoleo_EsteAno = 0
    ValorISVCO2Gasoleo_ProximoAno = 0
    ValorISVCO2Gasolina_EsteAno = 0
    ValorISVCO2Gasolina_ProximoAno = 0
# vou calcular o valor da componente ambiental, o CO2
    if (DadosISVCO2 > 0):

        # cálculo do CO2 em 2019, com os escalões de 2019 que são diferentes dos de 2020 por causa do WLTP
        if (DadosISVCO2 <= 79):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 5.24) - 398.07
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 4.23) - 391.03
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 1.56) - 10.43
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 0.44) - 39
        elif (DadosISVCO2 >= 80 and DadosISVCO2 <= 95):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 21.26) - 1676.38
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 4.19) - 387.16
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 1.56) - 10.43
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 0.44) - 39
        elif (DadosISVCO2 >= 96 and DadosISVCO2 <= 99):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 71.83) - 6524.16
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 4.19) - 387.16
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 1.56) - 10.43
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 0.44) - 39
        elif (DadosISVCO2 >= 100 and DadosISVCO2 <= 110):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 71.83) - 6524.16
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 7.33) - 680.91
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 1.56) - 10.43
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 0.44) - 39
        elif (DadosISVCO2 >= 111 and DadosISVCO2 <= 115):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 71.83) - 6524.16
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 7.33) - 680.91
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 17.2) - 1728.32
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 1) - 105
        elif (DadosISVCO2 >= 116 and DadosISVCO2 <= 120):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 71.83) - 6524.16
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 47.65) - 5353.01
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 17.2) - 1728.32
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 1.25) - 134
        elif (DadosISVCO2 >= 121 and DadosISVCO2 <= 130):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 159.33) - 17158.92
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 47.65) - 5353.01
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 58.97) - 6673.96
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 4.78) - 561.4
        elif (DadosISVCO2 >= 131 and DadosISVCO2 <= 140):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 159.33) - 17158.92
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 47.65) - 5353.01
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 58.97) - 6673.96
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 5.79) - 691.55
        elif (DadosISVCO2 >= 141 and DadosISVCO2 <= 145):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 177.19) - 19694.01
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 47.65) - 5353.01
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 115.78) - 14580
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 5.79) - 691.55
        elif (DadosISVCO2 >= 146 and DadosISVCO2 <= 150):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 177.19) - 19694.01
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 55.52) - 6473.88
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 115.5) - 14580
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 37.66) - 5276.5
        elif (DadosISVCO2 >= 151 and DadosISVCO2 <= 160):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 177.19) - 19694.01
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 55.52) - 6473.88
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 145.8) - 19200
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 37.66) - 5276.5
        elif (DadosISVCO2 >= 161 and DadosISVCO2 <= 170):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 243.38) - 30326.67
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 55.52) - 6473.88
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 201) - 26500
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 37.66) - 5276.5
        elif (DadosISVCO2 >= 171 and DadosISVCO2 <= 175):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 243.38) - 30326.67
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 55.52) - 6473.88
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 248.5) - 33536.42
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 37.66) - 5276.5
        elif (DadosISVCO2 >= 176 and DadosISVCO2 <= 190):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 243.38) - 30326.67
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 141.42) - 21422.47
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 248.5) - 33536.42
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 46.58) - 6571.1
        elif (DadosISVCO2 >= 191 and DadosISVCO2 <= 195):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 243.38) - 30326.67
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 141.42) - 21422.47
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 256) - 34700
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 46.58) - 6571.1
        elif (DadosISVCO2 >= 196 and DadosISVCO2 <= 235):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 243.38) - 30326.67				
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 186.47) - 30274.29
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 256) - 34700
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 175) - 31000
        elif (DadosISVCO2 >= 236):
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 243.38) - 30326.67				
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 186.47) - 30274.29
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 256) - 34700
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 212) - 38000

        if (DadosISVCO2_ProximoAno <= 79):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 5.78) - 439.04
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 4.62) - 427
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 1.72) - 11.50
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 0.44) - 43.02
        elif (DadosISVCO2_ProximoAno >= 80 and DadosISVCO2_ProximoAno <= 95):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 23.45) - 1848.58
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 4.62) - 427
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 1.72) - 11.50
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 0.44) - 43.02
        elif (DadosISVCO2_ProximoAno >= 96 and DadosISVCO2_ProximoAno <= 99):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 79.22) - 7195.63
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 4.62) - 427
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 1.72) - 11.50
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 0.44) - 43.02
        elif (DadosISVCO2_ProximoAno >= 100 and DadosISVCO2_ProximoAno <= 110):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 79.22) - 7195.63
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 8.09) - 750.99
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 1.72) - 11.50
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 0.44) - 43.02
        elif (DadosISVCO2_ProximoAno >= 111 and DadosISVCO2_ProximoAno <= 115):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 79.22) - 7195.63
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 8.09) - 750.99
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 18.96) - 1906.19
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 1.10) - 115.80
        elif (DadosISVCO2_ProximoAno >= 116 and DadosISVCO2_ProximoAno <= 120):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 79.22) - 7195.63
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 52.56) - 5903.94
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 18.96) - 1906.19
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 1.38) - 147.79
        elif (DadosISVCO2_ProximoAno >= 121 and DadosISVCO2_ProximoAno <= 130):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 175.73) - 18924.92
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 52.56) - 5903.94
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 65.04) - 7360.85
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 5.27) - 619.17
        elif (DadosISVCO2_ProximoAno >= 131 and DadosISVCO2_ProximoAno <= 140):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 175.73) - 18924.92
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 52.56) - 5903.94
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 65.04) - 7360.85
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 6.38) - 762.73
        elif (DadosISVCO2_ProximoAno >= 141 and DadosISVCO2_ProximoAno <= 145):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 195.43) - 21720.92
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 52.56) - 5903.94
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 127.40) - 16080.57
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 6.38) - 762.73
        elif (DadosISVCO2_ProximoAno >= 146 and DadosISVCO2_ProximoAno <= 150):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 195.43) - 21720.92
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 61.24) - 7140.17
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 127.40) - 16080.57
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 41.54) - 5819.56
        elif (DadosISVCO2_ProximoAno >= 151 and DadosISVCO2_ProximoAno <= 160):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 195.43) - 21720.92
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 61.24) - 7140.17
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 160.81) - 21176.06
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 41.54) - 5819.56
        elif (DadosISVCO2_ProximoAno >= 161 and DadosISVCO2_ProximoAno <= 170):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 268.42) - 33447.90
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 61.24) - 7140.17
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 221.69) - 29227.38
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 41.54) - 5819.56
        elif (DadosISVCO2_ProximoAno >= 171 and DadosISVCO2_ProximoAno <= 175):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 268.42) - 33447.90
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 61.24) - 7140.17
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 274.08) - 36987.98
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 41.54) - 5819.56
        elif (DadosISVCO2_ProximoAno >= 176 and DadosISVCO2_ProximoAno <= 190):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 268.42) - 33447.90
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 155.97) - 23627.27
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 274.08) - 36987.98
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 51.38) - 7247.39
        elif (DadosISVCO2_ProximoAno >= 191 and DadosISVCO2_ProximoAno <= 195):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 268.42) - 33447.90
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 155.97) - 23627.27
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 282.35) - 38271.32
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 51.38) - 7247.39
        elif (DadosISVCO2_ProximoAno >= 196 and DadosISVCO2_ProximoAno <= 235):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 268.42) - 33447.90
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 205.65) - 33390.12
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 282.35) - 38271.32
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 193.01) - 34190.52
        elif (DadosISVCO2_ProximoAno >= 236):
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 268.42) - 33447.90
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 205.65) - 33390.12
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 282.35) - 38271.32
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 233.81) - 41910.96
    # agora separamos o combustível para apresentar o resultado
    if (DadosCombustivel == "Gasoleo"):
            ValorISVCO2_EsteAno = ValorISVCO2Gasoleo_EsteAno
            ValorISVCO2_ProximoAno = ValorISVCO2Gasoleo_ProximoAno
    else:
            ValorISVCO2_EsteAno = ValorISVCO2Gasolina_EsteAno
            ValorISVCO2_ProximoAno = ValorISVCO2Gasolina_ProximoAno
    # aplicamos o desconto dos híbridos à componente ambiental 
    ValorISVCO2_EsteAno = ValorISVCO2_EsteAno * BeneficioHibrido
    ValorISVCO2_ProximoAno = ValorISVCO2_ProximoAno * BeneficioHibrido
# vamos calcular a componente CO2 com os descontos da idade
    # novo
    ValorISVCO2Novo_EsteAno = ValorISVCO2_EsteAno
    ValorISVCO2Novo_ProximoAno = ValorISVCO2_ProximoAno
    # até 6 meses
    ValorISVCO2Ate6Meses_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeAte6Meses)
    ValorISVCO2Ate6Meses_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeAte6Meses)
    ValorISVTotalAte6Meses_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeAte6Meses)
    # 6 meses a 1 ano
    ValorISVCO2Mais6Mesesa1Ano_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais6Mesesa1Ano)
    ValorISVCO2Mais6Mesesa1Ano_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais6Mesesa1Ano)
    ValorISVTotalMais6Mesesa1Ano_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais6Mesesa1Ano)
    # 1 a 2 anos
    ValorISVCO2Mais1a2Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais1a2Anos)
    ValorISVCO2Mais1a2Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais1a2Anos)
    ValorISVTotalMais1a2Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais1a2Anos)
    # 2 a 3 anos
    ValorISVCO2Mais2a3Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais2a3Anos)
    ValorISVCO2Mais2a3Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais2a3Anos)
    ValorISVTotalMais2a3Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais2a3Anos)
    # 3 a 4 anos
    ValorISVCO2Mais3a4Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais3a4Anos)
    ValorISVCO2Mais3a4Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais3a4Anos)
    ValorISVTotalMais3a4Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais3a4Anos)
    # 4 a 5 anos
    ValorISVCO2Mais4a5Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais4a5Anos)
    ValorISVCO2Mais4a5Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais4a5Anos)
    ValorISVTotalMais4a5Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais4a5Anos)
    # 5 a 6 anos
    ValorISVCO2Mais5a6Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais5a6Anos)
    ValorISVCO2Mais5a6Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais5a6Anos)
    ValorISVTotalMais5a6Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais5a6Anos)
    # 6 a 7 anos
    ValorISVCO2Mais6a7Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais6a7Anos)
    ValorISVCO2Mais6a7Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais6a7Anos)
    ValorISVTotalMais6a7Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais6a7Anos)
    # 7 a 8 anos
    ValorISVCO2Mais7a8Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais7a8Anos)
    ValorISVCO2Mais7a8Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais7a8Anos)
    ValorISVTotalMais7a8Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais7a8Anos)
    # 8 a 9 anos
    ValorISVCO2Mais8a9Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais8a9Anos)
    ValorISVCO2Mais8a9Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais8a9Anos)
    ValorISVTotalMais8a9Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais8a9Anos)
    # 9 a 10 anos
    ValorISVCO2Mais9a10Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais9a10Anos)
    ValorISVCO2Mais9a10Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais9a10Anos)
    ValorISVTotalMais9a10Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais9a10Anos)
    # 10 a 11 anos
    ValorISVCO2Mais10a11Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais10a11Anos)
    ValorISVCO2Mais10a11Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais10a11Anos)
    ValorISVTotalMais10a11Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais10a11Anos)
    # 11 a 12 anos
    ValorISVCO2Mais11a12Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais11a12Anos)
    ValorISVCO2Mais11a12Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais11a12Anos)
    ValorISVTotalMais11a12Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais11a12Anos)
    # 12 a 13 anos
    ValorISVCO2Mais12a13Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais12a13Anos)
    ValorISVCO2Mais12a13Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais12a13Anos)
    ValorISVTotalMais12a13Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais12a13Anos)
    # 13 a 14 anos
    ValorISVCO2Mais13a14Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais13a14Anos)
    ValorISVCO2Mais13a14Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais13a14Anos)
    ValorISVTotalMais13a14Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais13a14Anos)
    # 14 a 15 anos
    ValorISVCO2Mais14a15Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais14a15Anos)
    ValorISVCO2Mais14a15Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais14a15Anos)
    ValorISVTotalMais14a15Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais14a15Anos)
    # Mais de 15 anos
    ValorISVCO2Mais15Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais15Anos)
    ValorISVCO2Mais15Anos_ProximoAno = ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais15Anos)
    ValorISVTotalMais15Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais15Anos)

# vamos calcular o IVA
    ValorIVANovo_EsteAno = (ValorISVcm3_EsteAno + ValorISVCO2_EsteAno) * ValorIVA
    ValorIVANovo_ProximoAno = (ValorISVcm3_ProximoAno + ValorISVCO2_ProximoAno) * ValorIVA
    ValorIVANaoUE_EsteAno = (ValorISVcm3_EsteAno + ValorISVCO2_EsteAno + ValorTaxas + ValorCarro) * ValorIVA
    ValorIVANaoUE_ProximoAno = (ValorISVcm3_ProximoAno + ValorISVCO2_ProximoAno + ValorTaxas + ValorCarro) * ValorIVA
    ValorIVAAte6Meses_EsteAno = (ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeAte6Meses) + ValorISVCO2_EsteAno + ValorCarro) * ValorIVA
    ValorIVAAte6Meses_ProximoAno = (ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeAte6Meses) + ValorISVCO2_ProximoAno + ValorCarro) * ValorIVA
    
# vamos somar todas as parcelas, cilindrada, CO2, IVA e custos
    # novo
    ValorISVNovo_EsteAno = (ValorISVcm3_EsteAno + ValorISVCO2_EsteAno)
    ValorISVNovo_ProximoAno = (ValorISVcm3_ProximoAno + ValorISVCO2_ProximoAno)
    ValorTotalNovo_EsteAno = ((ValorISVcm3_EsteAno + ValorISVCO2_EsteAno) * ValorPercentagemIVA)
    ValorTotalNovo_ProximoAno = ((ValorISVcm3_ProximoAno + ValorISVCO2_ProximoAno) * ValorPercentagemIVA)
    ValorTotalNovo_DiferencaAnos = ValorTotalNovo_ProximoAno - ValorTotalNovo_EsteAno
    # não UE
    ValorTotalNaoUE_EsteAno = (ValorISVcm3_EsteAno + ValorISVCO2_EsteAno + ValorTaxas + ValorIVANaoUE_EsteAno + ValorDespesasImportacao)
    ValorTotalNaoUE_ProximoAno = (ValorISVcm3_ProximoAno + ValorISVCO2_ProximoAno + ValorTaxas + ValorIVANaoUE_ProximoAno + ValorDespesasImportacao)
    ValorTotalNaoUE_DiferencaAnos = ValorTotalNaoUE_ProximoAno - ValorTotalNaoUE_EsteAno
    # até 6 meses
    ValorISVAte6Meses_EsteAno = (ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeAte6Meses) + ValorISVCO2_EsteAno)
    ValorISVAte6Meses_ProximoAno = (ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeAte6Meses) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeAte6Meses)))
    ValorTotalAte6Meses_EsteAno = ((ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeAte6Meses) + ValorISVCO2_EsteAno + ValorCarro) * ValorPercentagemIVA) + ValorDespesasImportacao
    ValorTotalAte6Meses_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeAte6Meses) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeAte6Meses)) + ValorCarro) * ValorPercentagemIVA) + ValorDespesasImportacao
    ValorTotalAte6Meses_DiferencaAnos = ValorTotalAte6Meses_ProximoAno - ValorTotalAte6Meses_EsteAno
    ValorTotalAte6Meses_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeAte6Meses) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeAte6Meses)) + ValorCarro) * ValorPercentagemIVA) + ValorDespesasImportacao
    ValorTotalAte6Meses_DiferencaFuturo = ValorTotalAte6Meses_ProximoAno - ValorTotalAte6Meses_ProximoAnoFuturo
    # 6 meses a 1 ano
    ValorTotalMais6Mesesa1Ano_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais6Mesesa1Ano) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais6Mesesa1Ano_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais6Mesesa1Ano) + ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais6Mesesa1Ano) + ValorCarro + ValorDespesasImportacao
    ValorTotalMais6Mesesa1Ano_DiferencaAnos = ValorTotalMais6Mesesa1Ano_ProximoAno - ValorTotalMais6Mesesa1Ano_EsteAno
    ValorTotalMais6Mesesa1Ano_ProximoAnoFuturo = (ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais6Mesesa1Ano) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais6Mesesa1Ano)) + ValorCarro) + ValorDespesasImportacao
    ValorTotalMais6Mesesa1Ano_DiferencaFuturo = ValorTotalMais6Mesesa1Ano_ProximoAno - ValorTotalMais6Mesesa1Ano_ProximoAnoFuturo
    # 1 a 2 anos
    ValorTotalMais1a2Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais1a2Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais1a2Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais1a2Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais1a2Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais1a2Anos_DiferencaAnos = ValorTotalMais1a2Anos_ProximoAno - ValorTotalMais1a2Anos_EsteAno
    ValorTotalMais1a2Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais1a2Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais1a2Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais1a2Anos_DiferencaFuturo = ValorTotalMais1a2Anos_ProximoAno - ValorTotalMais1a2Anos_ProximoAnoFuturo
    # 2 a 3 anos
    ValorTotalMais2a3Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais2a3Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais2a3Anos_ProximoAno = (ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais2a3Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais2a3Anos)) + ValorCarro) + ValorDespesasImportacao
    ValorTotalMais2a3Anos_DiferencaAnos = ValorTotalMais2a3Anos_ProximoAno - ValorTotalMais2a3Anos_EsteAno
    ValorTotalMais2a3Anos_ProximoAnoFuturo = (ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais2a3Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais2a3Anos)) + ValorCarro) + ValorDespesasImportacao
    ValorTotalMais2a3Anos_DiferencaFuturo = ValorTotalMais2a3Anos_ProximoAno - ValorTotalMais2a3Anos_ProximoAnoFuturo
    # 3 a 4 anos
    ValorTotalMais3a4Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais3a4Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais3a4Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais3a4Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais3a4Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais3a4Anos_DiferencaAnos = ValorTotalMais3a4Anos_ProximoAno - ValorTotalMais3a4Anos_EsteAno
    ValorTotalMais3a4Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais3a4Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais3a4Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais3a4Anos_DiferencaFuturo = ValorTotalMais3a4Anos_ProximoAno - ValorTotalMais3a4Anos_ProximoAnoFuturo
    # 4 a 5 anos
    ValorTotalMais4a5Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais4a5Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais4a5Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais4a5Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais4a5Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais4a5Anos_DiferencaAnos = ValorTotalMais4a5Anos_ProximoAno - ValorTotalMais4a5Anos_EsteAno
    ValorTotalMais4a5Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais4a5Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais4a5Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais4a5Anos_DiferencaFuturo = ValorTotalMais4a5Anos_ProximoAno - ValorTotalMais4a5Anos_ProximoAnoFuturo
    # 5 a 6 anos
    ValorTotalMais5a6Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais5a6Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais5a6Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais5a6Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais5a6Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais5a6Anos_DiferencaAnos = ValorTotalMais5a6Anos_ProximoAno - ValorTotalMais5a6Anos_EsteAno
    ValorTotalMais5a6Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais5a6Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais5a6Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais5a6Anos_DiferencaFuturo = ValorTotalMais5a6Anos_ProximoAno - ValorTotalMais5a6Anos_ProximoAnoFuturo
    # 6 a 7 anos
    ValorTotalMais6a7Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais6a7Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais6a7Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais6a7Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais6a7Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais6a7Anos_DiferencaAnos = ValorTotalMais6a7Anos_ProximoAno - ValorTotalMais6a7Anos_EsteAno
    ValorTotalMais6a7Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais6a7Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais6a7Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais6a7Anos_DiferencaFuturo = ValorTotalMais6a7Anos_ProximoAno - ValorTotalMais6a7Anos_ProximoAnoFuturo
    # 7 a 8 anos
    ValorTotalMais7a8Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais7a8Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais7a8Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais7a8Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais7a8Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais7a8Anos_DiferencaAnos = ValorTotalMais7a8Anos_ProximoAno - ValorTotalMais7a8Anos_EsteAno
    ValorTotalMais7a8Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais7a8Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais7a8Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais7a8Anos_DiferencaFuturo = ValorTotalMais7a8Anos_ProximoAno - ValorTotalMais7a8Anos_ProximoAnoFuturo
    # 8 a 9 anos
    ValorTotalMais8a9Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais8a9Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais8a9Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais8a9Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais8a9Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais8a9Anos_DiferencaAnos = ValorTotalMais8a9Anos_ProximoAno - ValorTotalMais8a9Anos_EsteAno
    ValorTotalMais8a9Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais8a9Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais8a9Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais8a9Anos_DiferencaFuturo = ValorTotalMais8a9Anos_ProximoAno - ValorTotalMais8a9Anos_ProximoAnoFuturo
    # 9 a 10 anos
    ValorTotalMais9a10Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais9a10Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais9a10Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais9a10Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais9a10Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais9a10Anos_DiferencaAnos = ValorTotalMais9a10Anos_ProximoAno - ValorTotalMais9a10Anos_EsteAno
    ValorTotalMais9a10Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais9a10Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais9a10Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais9a10Anos_DiferencaFuturo = ValorTotalMais9a10Anos_ProximoAno - ValorTotalMais9a10Anos_ProximoAnoFuturo
    # 10 a 11 anos
    ValorTotalMais10a11Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais10a11Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais10a11Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais10a11Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais10a11Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais10a11Anos_DiferencaAnos = ValorTotalMais10a11Anos_ProximoAno - ValorTotalMais10a11Anos_EsteAno
    ValorTotalMais10a11Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais10a11Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais10a11Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais10a11Anos_DiferencaFuturo = ValorTotalMais10a11Anos_ProximoAno - ValorTotalMais10a11Anos_ProximoAnoFuturo
    # 11 a 12 anos
    ValorTotalMais11a12Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais11a12Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais11a12Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais11a12Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais11a12Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais11a12Anos_DiferencaAnos = ValorTotalMais11a12Anos_ProximoAno - ValorTotalMais11a12Anos_EsteAno
    ValorTotalMais11a12Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais11a12Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais11a12Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais11a12Anos_DiferencaFuturo = ValorTotalMais11a12Anos_ProximoAno - ValorTotalMais11a12Anos_ProximoAnoFuturo
    # 12 a 13 anos
    ValorTotalMais12a13Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais12a13Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais12a13Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais12a13Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais12a13Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais12a13Anos_DiferencaAnos = ValorTotalMais12a13Anos_ProximoAno - ValorTotalMais12a13Anos_EsteAno
    ValorTotalMais12a13Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais12a13Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais12a13Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais12a13Anos_DiferencaFuturo = ValorTotalMais12a13Anos_ProximoAno - ValorTotalMais12a13Anos_ProximoAnoFuturo
    # 13 a 14 anos
    ValorTotalMais13a14Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais13a14Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais13a14Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais13a14Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais13a14Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais13a14Anos_DiferencaAnos = ValorTotalMais13a14Anos_ProximoAno - ValorTotalMais13a14Anos_EsteAno
    ValorTotalMais13a14Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais13a14Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais13a14Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais13a14Anos_DiferencaFuturo = ValorTotalMais13a14Anos_ProximoAno - ValorTotalMais13a14Anos_ProximoAnoFuturo
    # 14 a 15 anos
    ValorTotalMais14a15Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais14a15Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais14a15Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais14a15Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais14a15Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais14a15Anos_DiferencaAnos = ValorTotalMais14a15Anos_ProximoAno - ValorTotalMais14a15Anos_EsteAno
    ValorTotalMais14a15Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais14a15Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais14a15Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais14a15Anos_DiferencaFuturo = ValorTotalMais14a15Anos_ProximoAno - ValorTotalMais14a15Anos_ProximoAnoFuturo
    # mais de 15 anos
    ValorTotalMais15Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais15Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao
    ValorTotalMais15Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais15Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais15Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais15Anos_DiferencaAnos = ValorTotalMais15Anos_ProximoAno - ValorTotalMais15Anos_EsteAno
    ValorTotalMais15Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais15Anos) + (ValorISVCO2_ProximoAno - abs(ValorISVCO2_ProximoAno * DescontoIdadeMais15Anos)) + ValorCarro)) + ValorDespesasImportacao
    ValorTotalMais15Anos_DiferencaFuturo = ValorTotalMais15Anos_ProximoAno - ValorTotalMais15Anos_ProximoAnoFuturo
# vamos apresentar os resultados na coluna à direita
    if (DadosISVcm3 > 100 and DadosISVCO2 > 10):

        # returns the year (four digits)
        date = datetime.date.today()
        currentYear = date.strftime("%Y")
        carAge = int(currentYear) - productionYear
        if carAge == 0:
            result = round(float(max(ValorISVMinimo,ValorTotalMais6Mesesa1Ano_EsteAno)), 2)
        elif carAge == 1:
            result = round(float(max(ValorISVMinimo,ValorTotalMais1a2Anos_EsteAno)), 2)
        elif carAge == 2:
            result = round(float(max(ValorISVMinimo,ValorTotalMais2a3Anos_EsteAno)), 2)
        elif carAge == 3:
            result = round(float(max(ValorISVMinimo,ValorTotalMais3a4Anos_EsteAno)), 2)
        elif carAge == 4:
            result = round(float(max(ValorISVMinimo,ValorTotalMais4a5Anos_EsteAno)), 2)
        elif carAge == 5:
            result = round(float(max(ValorISVMinimo,ValorTotalMais5a6Anos_EsteAno)), 2)
        elif carAge == 6:
            result = round(float(max(ValorISVMinimo,ValorTotalMais6a7Anos_EsteAno)), 2)
        elif carAge == 7:
            result = round(float(max(ValorISVMinimo,ValorTotalMais7a8Anos_EsteAno)), 2)
        elif carAge == 8:
            result = round(float(max(ValorISVMinimo,ValorTotalMais8a9Anos_EsteAno)), 2)
        elif carAge == 9:
            result = round(float(max(ValorISVMinimo,ValorTotalMais9a10Anos_EsteAno)), 2)
        elif carAge == 10:
            result = round(float(max(ValorISVMinimo,ValorTotalMais10a11Anos_EsteAno)), 2)
        elif carAge == 11:
            result = round(float(max(ValorISVMinimo,ValorTotalMais11a12Anos_EsteAno)), 2)
        elif carAge == 12:
            result = round(float(max(ValorISVMinimo,ValorTotalMais12a13Anos_EsteAno)), 2)
        elif carAge == 13:
            result = round(float(max(ValorISVMinimo,ValorTotalMais13a14Anos_EsteAno)), 2)
        elif carAge == 14:
            result = round(float(max(ValorISVMinimo,ValorTotalMais14a15Anos_EsteAno)), 2)
        else:
            result = round(float(max(ValorISVMinimo,ValorTotalMais15Anos_EsteAno)), 2)

        return result