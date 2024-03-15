var Calcular = function(displacement, emissions, fuel, price, productionYear) {

// Defino as variáveis
// preciso mesmo da palavra valor à frente das variáveis?!

// variável da cilindrada do ISV, será boa ideia criar duas variáveis, uma para cada imposto? é que a variável não muda, é sempre a mesma!
    var DadosISVcm3 = 0;
// variável do CO2
    var DadosISVCO2 = 0;
// variável do combustível para poder apresentar o feedback na simulação
    var DadosCombustivel = "";
// defino como 10% o valor das taxas aduaneiras - é o máximo possível
    var TaxasAduaneirasPercentagem = 0.1;
// o valor mínimo do ISV é sempre 100€, tenho que definir essa variável, assim como o valor do IVA para o caso dos novos e dos importados fora UE
    var ValorISVMinimo = 100;
    var ValorPercentagemIVA = 1.23;
    var ValorIVA = 0.23;
// preciso do valor do carro para apresentar resultados com o valor incluído, para apresentar um "PVP", para calcular o IVA e as taxas aduaneiras
    var ValorCarro = 0;
    var ValorTaxas = 0;
    var ValorDespesasImportacao = 0;
    var SimboloEuro = "€";
    var DadosISVCO2WLTP = "";
// defino as variáveis com os descontos da idade cilindrada
    var DescontoIdadeAte6Meses = 0.1;
    var DescontoIdadeMais6Mesesa1Ano = 0.1;
    var DescontoIdadeMais1a2Anos = 0.2;
    var DescontoIdadeMais2a3Anos = 0.28;
    var DescontoIdadeMais3a4Anos = 0.35;
    var DescontoIdadeMais4a5Anos = 0.43;
    var DescontoIdadeMais5a6Anos = 0.52;
    var DescontoIdadeMais6a7Anos = 0.6;
    var DescontoIdadeMais7a8Anos = 0.65;
    var DescontoIdadeMais8a9Anos = 0.7;
    var DescontoIdadeMais9a10Anos = 0.75;
    var DescontoIdadeMais10a11Anos = 0.8;
    var DescontoIdadeMais11a12Anos = 0.8;
    var DescontoIdadeMais12a13Anos = 0.8;
    var DescontoIdadeMais13a14Anos = 0.8;
    var DescontoIdadeMais14a15Anos = 0.8;
    var DescontoIdadeMais15Anos = 0.8;

// defino as variáveis com os descontos da idade CO2
    var DescontoCO2IdadeAte6Meses = 0.10;
    var DescontoCO2IdadeMais6Mesesa1Ano = 0.10;
    var DescontoCO2IdadeMais1a2Anos = 0.10;
    var DescontoCO2IdadeMais2a3Anos = 0.20;
    var DescontoCO2IdadeMais3a4Anos = 0.20;
    var DescontoCO2IdadeMais4a5Anos = 0.28;
    var DescontoCO2IdadeMais5a6Anos = 0.28;
    var DescontoCO2IdadeMais6a7Anos = 0.35;
    var DescontoCO2IdadeMais7a8Anos = 0.43;
    var DescontoCO2IdadeMais8a9Anos = 0.43;
    var DescontoCO2IdadeMais9a10Anos = 0.52;
    var DescontoCO2IdadeMais10a11Anos = 0.60;
    var DescontoCO2IdadeMais11a12Anos = 0.60;
    var DescontoCO2IdadeMais12a13Anos = 0.65;
    var DescontoCO2IdadeMais13a14Anos = 0.70;
    var DescontoCO2IdadeMais14a15Anos = 0.75;
    var DescontoCO2IdadeMais15Anos = 0.8;
// os benefícios fiscais são dados como x% do valor do ISV, aqui indico as variáveis dos benefícios que não passam de percentagens, daí terem que ser todas 1 inicialmente
    var BeneficioHibridoNormalPercentagem = 0.6;
    var BeneficioHibridoPlugInPercentagem = 0.25;
    var BeneficioHibrido = 1;
// os valores em € das duas componentes
    var ValorISVcm3_EsteAno = 0;
    var ValorISVcm3_ProximoAno = 0;
    var ValorISVCO2_EsteAno = 0;
    var ValorISVCO2_ProximoAno = 0;
    var ValorISVTotal_EsteAno = ValorISVcm3_EsteAno + ValorISVCO2_EsteAno;
    var ValorISVTotal_ProximoAno = ValorISVcm3_ProximoAno + ValorISVCO2_ProximoAno;
    
// Vou buscar os dados aos campos se estiverem preenchidos e atribuo-os às variáveis

// vou buscar a cilindrada ao campo
    if (displacement > 0) {
        var DadosISVcm3 = displacement;
    };
// agora vou buscar o CO2 ao campo
    var DadosISVCO2 = emissions;
    var DadosISVCO2_ProximoAno = emissions;
// vejo qual foi o combustível escolhido para definir uma variável para depois dar feedback ao utilizador do combustível que está activo para a simulação
    switch(fuel){
        case "Diesel":
            var DadosCombustivel = "Gasoleo";
        case "Petrol":
            var DadosCombustivel = "Gasolina";
        case "Hybrid-Petrol":
            var isHybrid = true;
        case "Hybrid-Diesel":
            var isHybrid = true;
        case "Hybrid-Plug-in":
            var isPluginHybrid = true;
    };
// vou buscar o valor do carro ao campo para apresentar a simulação com o valor do carro incluído, para calcular o valor das taxas aduaneiras a 10% e coloco/retiro os avisos para as importações fora UE
    if (price > 0) {
        var ValorCarro = price;
        var ValorTaxas = ValorCarro * TaxasAduaneirasPercentagem;
    }

// Cálculos preliminares

// desconto dado aos híbridos
    if (isHybrid) {
        BeneficioHibrido = BeneficioHibridoNormalPercentagem;
    };
    if (isPluginHybrid) {
        BeneficioHibrido = BeneficioHibridoPlugInPercentagem;
    };	

// vamos calcular a componente cilindrada que é comum ao NEDC e WLTP, coloco a operação lógica porque há pessoas que não preenchem a cilindrada e eu não quero apresentar simulações sem esse dado, o 100 é escolhido por ser um mínimo de 3 algarismos, ao mesmo tempo que preenche o campo, aparece o campo seguinte do CO2, tenho que definir dois anos para poder fazer as comparações entre orçamentos de estado
    if (DadosISVcm3 > 100) {
        if (DadosISVcm3 <= 1000) {
            ValorISVcm3_EsteAno = (DadosISVcm3 * 1.00) - 777.50;
            ValorISVcm3_ProximoAno = (DadosISVcm3 * 1.09) - 849.03;
        } else if (DadosISVcm3 <= 1250) {
            ValorISVcm3_EsteAno = (DadosISVcm3 * 1.08) - 779.02;
            ValorISVcm3_ProximoAno = (DadosISVcm3 * 1.18) - 850.69;
        } else if (DadosISVcm3 > 1250) {
            ValorISVcm3_EsteAno = (DadosISVcm3 * 5.13) - 5672.97
            ValorISVcm3_ProximoAno = (DadosISVcm3 * 5.61) - 6194.88
        };
    }
// aplico o desconto dos hibridos à componente cilindrada, será boa ideia aplicar este desconto só no fim em vez de o aplicar duas vezes às componentes? Se calhar sim, porque se isto muda para se aplicar o desconto a uma só componente em vez de à totalidade, fico pendurado
    var ValorISVcm3_EsteAno = ValorISVcm3_EsteAno * BeneficioHibrido;
    var ValorISVcm3_ProximoAno = ValorISVcm3_ProximoAno * BeneficioHibrido;
// vamos calcular a componente cilindrada com os descontos da idade
    // novo
    var ValorISVcm3Novo_EsteAno = ValorISVcm3_EsteAno;
    var ValorISVcm3Novo_ProximoAno = ValorISVcm3_ProximoAno;
    // até 6 meses
    var ValorISVcm3Ate6Meses_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeAte6Meses);
    var ValorISVcm3Ate6Meses_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeAte6Meses);
    var ValorISVTotalAte6Meses_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeAte6Meses);
    // 6 meses a 1 ano
    var ValorISVcm3Mais6Mesesa1Ano_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais6Mesesa1Ano);
    var ValorISVcm3Mais6Mesesa1Ano_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais6Mesesa1Ano);
    var ValorISVTotalMais6Mesesa1Ano_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais6Mesesa1Ano);
    // 1 a 2 anos
    var ValorISVcm3Mais1a2Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais1a2Anos);
    var ValorISVcm3Mais1a2Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais1a2Anos);
    var ValorISVTotalMais1a2Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais1a2Anos);
    // 2 a 3 anos
    var ValorISVcm3Mais2a3Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais2a3Anos);
    var ValorISVcm3Mais2a3Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais2a3Anos);
    var ValorISVTotalMais2a3Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais2a3Anos);
    // 3 a 4 anos
    var ValorISVcm3Mais3a4Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais3a4Anos);
    var ValorISVcm3Mais3a4Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais3a4Anos);
    var ValorISVTotalMais3a4Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais3a4Anos);
    // 4 a 5 anos
    var ValorISVcm3Mais4a5Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais4a5Anos);
    var ValorISVcm3Mais4a5Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais4a5Anos);
    var ValorISVTotalMais4a5Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais4a5Anos);
    // 5 a 6 anos
    var ValorISVcm3Mais5a6Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais5a6Anos);
    var ValorISVcm3Mais5a6Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais5a6Anos);
    var ValorISVTotalMais5a6Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais5a6Anos);
    // 6 a 7 anos
    var ValorISVcm3Mais6a7Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais6a7Anos);
    var ValorISVcm3Mais6a7Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais6a7Anos);
    var ValorISVTotalMais6a7Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais6a7Anos);
    // 7 a 8 anos
    var ValorISVcm3Mais7a8Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais7a8Anos);
    var ValorISVcm3Mais7a8Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais7a8Anos);
    var ValorISVTotalMais7a8Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais7a8Anos);
    // 8 a 9 anos
    var ValorISVcm3Mais8a9Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais8a9Anos);
    var ValorISVcm3Mais8a9Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais8a9Anos);
    var ValorISVTotalMais8a9Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais8a9Anos);
    // 9 a 10 anos
    var ValorISVcm3Mais9a10Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais9a10Anos);
    var ValorISVcm3Mais9a10Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais9a10Anos);
    var ValorISVTotalMais9a10Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais9a10Anos);
    // 10 a 11 anos
    var ValorISVcm3Mais10a11Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais10a11Anos);
    var ValorISVcm3Mais10a11Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais10a11Anos);
    var ValorISVTotalMais10a11Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais10a11Anos);
    // 11 a 12 anos
    var ValorISVcm3Mais11a12Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais11a12Anos);
    var ValorISVcm3Mais11a12Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais11a12Anos);
    var ValorISVTotalMais11a12Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais11a12Anos);
    // 12 a 13 anos
    var ValorISVcm3Mais12a13Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais12a13Anos);
    var ValorISVcm3Mais12a13Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais12a13Anos);
    var ValorISVTotalMais12a13Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais12a13Anos);
    // 13 a 14 anos
    var ValorISVcm3Mais13a14Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais13a14Anos);
    var ValorISVcm3Mais13a14Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais13a14Anos);
    var ValorISVTotalMais13a14Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais13a14Anos);
    // 14 a 15 anos
    var ValorISVcm3Mais14a15Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais14a15Anos);
    var ValorISVcm3Mais14a15Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais14a15Anos);
    var ValorISVTotalMais14a15Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais14a15Anos);
    // mais de 15 anos
    var ValorISVcm3Mais15Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais15Anos);
    var ValorISVcm3Mais15Anos_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais15Anos);
    var ValorISVTotalMais15Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoIdadeMais15Anos);
// definir as variáveis do valor do CO2
    var ValorISVCO2Gasoleo_EsteAno = 0;
    var ValorISVCO2Gasoleo_ProximoAno = 0;
    var ValorISVCO2Gasolina_EsteAno = 0;
    var ValorISVCO2Gasolina_ProximoAno = 0;
// vou calcular o valor da componente ambiental, o CO2
    if (DadosISVCO2 > 0) {

        // cálculo do CO2 em 2019, com os escalões de 2019 que são diferentes dos de 2020 por causa do WLTP
        if (DadosISVCO2 <= 79) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 5.24) - 398.07;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 4.23) - 391.03;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 1.56) - 10.43;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 0.44) - 39;
        } else if (DadosISVCO2 >= 80 && DadosISVCO2 <= 95) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 21.26) - 1676.38;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 4.19) - 387.16;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 1.56) - 10.43;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 0.44) - 39;
        } else if (DadosISVCO2 >= 96 && DadosISVCO2 <= 99) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 71.83) - 6524.16;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 4.19) - 387.16;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 1.56) - 10.43;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 0.44) - 39;
        } else if (DadosISVCO2 >= 100 && DadosISVCO2 <= 110) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 71.83) - 6524.16;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 7.33) - 680.91;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 1.56) - 10.43;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 0.44) - 39;
        } else if (DadosISVCO2 >= 111 && DadosISVCO2 <= 115) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 71.83) - 6524.16;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 7.33) - 680.91;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 17.2) - 1728.32;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 1) - 105;
        } else if (DadosISVCO2 >= 116 && DadosISVCO2 <= 120) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 71.83) - 6524.16;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 47.65) - 5353.01;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 17.2) - 1728.32;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 1.25) - 134;
        } else if (DadosISVCO2 >= 121 && DadosISVCO2 <= 130) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 159.33) - 17158.92;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 47.65) - 5353.01;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 58.97) - 6673.96;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 4.78) - 561.4;
        } else if (DadosISVCO2 >= 131 && DadosISVCO2 <= 140) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 159.33) - 17158.92;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 47.65) - 5353.01;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 58.97) - 6673.96;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 5.79) - 691.55;
        } else if (DadosISVCO2 >= 141 && DadosISVCO2 <= 145) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 177.19) - 19694.01;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 47.65) - 5353.01;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 115.78) - 14580;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 5.79) - 691.55;
        } else if (DadosISVCO2 >= 146 && DadosISVCO2 <= 150) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 177.19) - 19694.01;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 55.52) - 6473.88;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 115.5) - 14580;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 37.66) - 5276.5;
        } else if (DadosISVCO2 >= 151 && DadosISVCO2 <= 160) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 177.19) - 19694.01;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 55.52) - 6473.88;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 145.8) - 19200;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 37.66) - 5276.5;
        } else if (DadosISVCO2 >= 161 && DadosISVCO2 <= 170) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 243.38) - 30326.67;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 55.52) - 6473.88;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 201) - 26500;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 37.66) - 5276.5;
        } else if (DadosISVCO2 >= 171 && DadosISVCO2 <= 175) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 243.38) - 30326.67;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 55.52) - 6473.88;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 248.5) - 33536.42;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 37.66) - 5276.5;
        } else if (DadosISVCO2 >= 176 && DadosISVCO2 <= 190) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 243.38) - 30326.67;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 141.42) - 21422.47;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 248.5) - 33536.42;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 46.58) - 6571.1;
        } else if (DadosISVCO2 >= 191 && DadosISVCO2 <= 195) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 243.38) - 30326.67;
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 141.42) - 21422.47;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 256) - 34700;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 46.58) - 6571.1;
        } else if (DadosISVCO2 >= 196 && DadosISVCO2 <= 235) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 243.38) - 30326.67;				
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 186.47) - 30274.29;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 256) - 34700;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 175) - 31000;
        } else if (DadosISVCO2 >= 236) {
            ValorISVCO2Gasoleo_EsteAno = (DadosISVCO2 * 243.38) - 30326.67;				
            ValorISVCO2Gasolina_EsteAno = (DadosISVCO2 * 186.47) - 30274.29;
            ValorISVCO2GasoleoWLTP_EsteAno = (DadosISVCO2 * 256) - 34700;
            ValorISVCO2GasolinaWLTP_EsteAno = (DadosISVCO2 * 212) - 38000;
        };
        if (DadosISVCO2_ProximoAno <= 79) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 5.78) - 439.04;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 4.62) - 427;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 1.72) - 11.50;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 0.44) - 43.02;
        } else if (DadosISVCO2_ProximoAno >= 80 && DadosISVCO2_ProximoAno <= 95) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 23.45) - 1848.58;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 4.62) - 427;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 1.72) - 11.50;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 0.44) - 43.02;
        } else if (DadosISVCO2_ProximoAno >= 96 && DadosISVCO2_ProximoAno <= 99) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 79.22) - 7195.63;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 4.62) - 427;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 1.72) - 11.50;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 0.44) - 43.02;
        } else if (DadosISVCO2_ProximoAno >= 100 && DadosISVCO2_ProximoAno <= 110) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 79.22) - 7195.63;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 8.09) - 750.99;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 1.72) - 11.50;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 0.44) - 43.02;
        } else if (DadosISVCO2_ProximoAno >= 111 && DadosISVCO2_ProximoAno <= 115) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 79.22) - 7195.63;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 8.09) - 750.99;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 18.96) - 1906.19;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 1.10) - 115.80;
        } else if (DadosISVCO2_ProximoAno >= 116 && DadosISVCO2_ProximoAno <= 120) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 79.22) - 7195.63;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 52.56) - 5903.94;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 18.96) - 1906.19;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 1.38) - 147.79;
        } else if (DadosISVCO2_ProximoAno >= 121 && DadosISVCO2_ProximoAno <= 130) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 175.73) - 18924.92;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 52.56) - 5903.94;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 65.04) - 7360.85;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 5.27) - 619.17;
        } else if (DadosISVCO2_ProximoAno >= 131 && DadosISVCO2_ProximoAno <= 140) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 175.73) - 18924.92;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 52.56) - 5903.94;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 65.04) - 7360.85;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 6.38) - 762.73;
        } else if (DadosISVCO2_ProximoAno >= 141 && DadosISVCO2_ProximoAno <= 145) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 195.43) - 21720.92;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 52.56) - 5903.94;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 127.40) - 16080.57;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 6.38) - 762.73;
        } else if (DadosISVCO2_ProximoAno >= 146 && DadosISVCO2_ProximoAno <= 150) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 195.43) - 21720.92;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 61.24) - 7140.17;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 127.40) - 16080.57;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 41.54) - 5819.56;
        } else if (DadosISVCO2_ProximoAno >= 151 && DadosISVCO2_ProximoAno <= 160) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 195.43) - 21720.92;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 61.24) - 7140.17;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 160.81) - 21176.06;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 41.54) - 5819.56;
        } else if (DadosISVCO2_ProximoAno >= 161 && DadosISVCO2_ProximoAno <= 170) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 268.42) - 33447.90;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 61.24) - 7140.17;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 221.69) - 29227.38;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 41.54) - 5819.56;
        } else if (DadosISVCO2_ProximoAno >= 171 && DadosISVCO2_ProximoAno <= 175) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 268.42) - 33447.90;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 61.24) - 7140.17;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 274.08) - 36987.98;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 41.54) - 5819.56;
        } else if (DadosISVCO2_ProximoAno >= 176 && DadosISVCO2_ProximoAno <= 190) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 268.42) - 33447.90;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 155.97) - 23627.27;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 274.08) - 36987.98;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 51.38) - 7247.39;
        } else if (DadosISVCO2_ProximoAno >= 191 && DadosISVCO2_ProximoAno <= 195) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 268.42) - 33447.90;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 155.97) - 23627.27;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 282.35) - 38271.32;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 51.38) - 7247.39;
        } else if (DadosISVCO2_ProximoAno >= 196 && DadosISVCO2_ProximoAno <= 235) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 268.42) - 33447.90;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 205.65) - 33390.12;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 282.35) - 38271.32;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 193.01) - 34190.52;
        } else if (DadosISVCO2_ProximoAno >= 236) {
            ValorISVCO2Gasoleo_ProximoAno = (DadosISVCO2_ProximoAno * 268.42) - 33447.90;
            ValorISVCO2Gasolina_ProximoAno = (DadosISVCO2_ProximoAno * 205.65) - 33390.12;
            ValorISVCO2GasoleoWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 282.35) - 38271.32;
            ValorISVCO2GasolinaWLTP_ProximoAno = (DadosISVCO2_ProximoAno * 233.81) - 41910.96;
        };
    };
    // agora separamos o combustível para apresentar o resultado
    if (DadosCombustivel == "Gasoleo") {
            ValorISVCO2_EsteAno = ValorISVCO2Gasoleo_EsteAno;
            ValorISVCO2_ProximoAno = ValorISVCO2Gasoleo_ProximoAno;
    } else {
            ValorISVCO2_EsteAno = ValorISVCO2Gasolina_EsteAno;
            ValorISVCO2_ProximoAno = ValorISVCO2Gasolina_ProximoAno;
    };
    // aplicamos o desconto dos híbridos à componente ambiental 
    ValorISVCO2_EsteAno = ValorISVCO2_EsteAno * BeneficioHibrido;
    ValorISVCO2_ProximoAno = ValorISVCO2_ProximoAno * BeneficioHibrido;
// vamos calcular a componente CO2 com os descontos da idade
    // novo
    var ValorISVCO2Novo_EsteAno = ValorISVCO2_EsteAno;
    var ValorISVCO2Novo_ProximoAno = ValorISVCO2_ProximoAno;
    // até 6 meses
    var ValorISVCO2Ate6Meses_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeAte6Meses);
    var ValorISVCO2Ate6Meses_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeAte6Meses);
    var ValorISVTotalAte6Meses_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeAte6Meses);
    // 6 meses a 1 ano
    var ValorISVCO2Mais6Mesesa1Ano_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais6Mesesa1Ano);
    var ValorISVCO2Mais6Mesesa1Ano_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais6Mesesa1Ano);
    var ValorISVTotalMais6Mesesa1Ano_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais6Mesesa1Ano);
    // 1 a 2 anos
    var ValorISVCO2Mais1a2Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais1a2Anos);
    var ValorISVCO2Mais1a2Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais1a2Anos);
    var ValorISVTotalMais1a2Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais1a2Anos);
    // 2 a 3 anos
    var ValorISVCO2Mais2a3Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais2a3Anos);
    var ValorISVCO2Mais2a3Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais2a3Anos);
    var ValorISVTotalMais2a3Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais2a3Anos);
    // 3 a 4 anos
    var ValorISVCO2Mais3a4Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais3a4Anos);
    var ValorISVCO2Mais3a4Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais3a4Anos);
    var ValorISVTotalMais3a4Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais3a4Anos);
    // 4 a 5 anos
    var ValorISVCO2Mais4a5Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais4a5Anos);
    var ValorISVCO2Mais4a5Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais4a5Anos);
    var ValorISVTotalMais4a5Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais4a5Anos);
    // 5 a 6 anos
    var ValorISVCO2Mais5a6Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais5a6Anos);
    var ValorISVCO2Mais5a6Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais5a6Anos);
    var ValorISVTotalMais5a6Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais5a6Anos);
    // 6 a 7 anos
    var ValorISVCO2Mais6a7Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais6a7Anos);
    var ValorISVCO2Mais6a7Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais6a7Anos);
    var ValorISVTotalMais6a7Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais6a7Anos);
    // 7 a 8 anos
    var ValorISVCO2Mais7a8Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais7a8Anos);
    var ValorISVCO2Mais7a8Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais7a8Anos);
    var ValorISVTotalMais7a8Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais7a8Anos);
    // 8 a 9 anos
    var ValorISVCO2Mais8a9Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais8a9Anos);
    var ValorISVCO2Mais8a9Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais8a9Anos);
    var ValorISVTotalMais8a9Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais8a9Anos);
    // 9 a 10 anos
    var ValorISVCO2Mais9a10Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais9a10Anos);
    var ValorISVCO2Mais9a10Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais9a10Anos);
    var ValorISVTotalMais9a10Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais9a10Anos);
    // 10 a 11 anos
    var ValorISVCO2Mais10a11Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais10a11Anos);
    var ValorISVCO2Mais10a11Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais10a11Anos);
    var ValorISVTotalMais10a11Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais10a11Anos);
    // 11 a 12 anos
    var ValorISVCO2Mais11a12Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais11a12Anos);
    var ValorISVCO2Mais11a12Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais11a12Anos);
    var ValorISVTotalMais11a12Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais11a12Anos);
    // 12 a 13 anos
    var ValorISVCO2Mais12a13Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais12a13Anos);
    var ValorISVCO2Mais12a13Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais12a13Anos);
    var ValorISVTotalMais12a13Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais12a13Anos);
    // 13 a 14 anos
    var ValorISVCO2Mais13a14Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais13a14Anos);
    var ValorISVCO2Mais13a14Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais13a14Anos);
    var ValorISVTotalMais13a14Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais13a14Anos);
    // 14 a 15 anos
    var ValorISVCO2Mais14a15Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais14a15Anos);
    var ValorISVCO2Mais14a15Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais14a15Anos);
    var ValorISVTotalMais14a15Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais14a15Anos);
    // Mais de 15 anos
    var ValorISVCO2Mais15Anos_EsteAno = ValorISVCO2_EsteAno - (ValorISVCO2_EsteAno * DescontoCO2IdadeMais15Anos);
    var ValorISVCO2Mais15Anos_ProximoAno = ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais15Anos);
    var ValorISVTotalMais15Anos_ProximoAno = ValorISVTotal_ProximoAno - (ValorISVTotal_ProximoAno * DescontoCO2IdadeMais15Anos);

// vamos calcular o IVA
    var ValorIVANovo_EsteAno = (ValorISVcm3_EsteAno + ValorISVCO2_EsteAno) * ValorIVA;
    var ValorIVANovo_ProximoAno = (ValorISVcm3_ProximoAno + ValorISVCO2_ProximoAno) * ValorIVA;
    var ValorIVANaoUE_EsteAno = (ValorISVcm3_EsteAno + ValorISVCO2_EsteAno + ValorTaxas + ValorCarro) * ValorIVA;
    var ValorIVANaoUE_ProximoAno = (ValorISVcm3_ProximoAno + ValorISVCO2_ProximoAno + ValorTaxas + ValorCarro) * ValorIVA;
    var ValorIVAAte6Meses_EsteAno = (ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeAte6Meses) + ValorISVCO2_EsteAno + ValorCarro) * ValorIVA;
    var ValorIVAAte6Meses_ProximoAno = (ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeAte6Meses) + ValorISVCO2_ProximoAno + ValorCarro) * ValorIVA;
    
// vamos somar todas as parcelas, cilindrada, CO2, IVA e custos
    // novo
    var ValorISVNovo_EsteAno = (ValorISVcm3_EsteAno + ValorISVCO2_EsteAno);
    var ValorISVNovo_ProximoAno = (ValorISVcm3_ProximoAno + ValorISVCO2_ProximoAno);
    var ValorTotalNovo_EsteAno = ((ValorISVcm3_EsteAno + ValorISVCO2_EsteAno) * ValorPercentagemIVA);
    var ValorTotalNovo_ProximoAno = ((ValorISVcm3_ProximoAno + ValorISVCO2_ProximoAno) * ValorPercentagemIVA);
    var ValorTotalNovo_DiferencaAnos = ValorTotalNovo_ProximoAno - ValorTotalNovo_EsteAno;
    // não UE
    var ValorTotalNaoUE_EsteAno = (ValorISVcm3_EsteAno + ValorISVCO2_EsteAno + ValorTaxas + ValorIVANaoUE_EsteAno + ValorDespesasImportacao);
    var ValorTotalNaoUE_ProximoAno = (ValorISVcm3_ProximoAno + ValorISVCO2_ProximoAno + ValorTaxas + ValorIVANaoUE_ProximoAno + ValorDespesasImportacao);
    var ValorTotalNaoUE_DiferencaAnos = ValorTotalNaoUE_ProximoAno - ValorTotalNaoUE_EsteAno;
    // até 6 meses
    var ValorISVAte6Meses_EsteAno = (ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeAte6Meses) + ValorISVCO2_EsteAno);
    var ValorISVAte6Meses_ProximoAno = (ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeAte6Meses) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeAte6Meses)));
    var ValorTotalAte6Meses_EsteAno = ((ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeAte6Meses) + ValorISVCO2_EsteAno + ValorCarro) * ValorPercentagemIVA) + ValorDespesasImportacao;
    var ValorTotalAte6Meses_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeAte6Meses) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeAte6Meses)) + ValorCarro) * ValorPercentagemIVA) + ValorDespesasImportacao;
    var ValorTotalAte6Meses_DiferencaAnos = ValorTotalAte6Meses_ProximoAno - ValorTotalAte6Meses_EsteAno;
    var ValorTotalAte6Meses_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeAte6Meses) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeAte6Meses)) + ValorCarro) * ValorPercentagemIVA) + ValorDespesasImportacao;
    var ValorTotalAte6Meses_DiferencaFuturo = ValorTotalAte6Meses_ProximoAno - ValorTotalAte6Meses_ProximoAnoFuturo;
    // 6 meses a 1 ano
    var ValorTotalMais6Mesesa1Ano_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais6Mesesa1Ano) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais6Mesesa1Ano_ProximoAno = ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais6Mesesa1Ano) + ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais6Mesesa1Ano) + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais6Mesesa1Ano_DiferencaAnos = ValorTotalMais6Mesesa1Ano_ProximoAno - ValorTotalMais6Mesesa1Ano_EsteAno;
    var ValorTotalMais6Mesesa1Ano_ProximoAnoFuturo = (ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais6Mesesa1Ano) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais6Mesesa1Ano)) + ValorCarro) + ValorDespesasImportacao;
    var ValorTotalMais6Mesesa1Ano_DiferencaFuturo = ValorTotalMais6Mesesa1Ano_ProximoAno - ValorTotalMais6Mesesa1Ano_ProximoAnoFuturo;
    // 1 a 2 anos
    var ValorTotalMais1a2Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais1a2Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais1a2Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais1a2Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais1a2Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais1a2Anos_DiferencaAnos = ValorTotalMais1a2Anos_ProximoAno - ValorTotalMais1a2Anos_EsteAno;
    var ValorTotalMais1a2Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais1a2Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais1a2Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais1a2Anos_DiferencaFuturo = ValorTotalMais1a2Anos_ProximoAno - ValorTotalMais1a2Anos_ProximoAnoFuturo;
    // 2 a 3 anos
    var ValorTotalMais2a3Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais2a3Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais2a3Anos_ProximoAno = (ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais2a3Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais2a3Anos)) + ValorCarro) + ValorDespesasImportacao;
    var ValorTotalMais2a3Anos_DiferencaAnos = ValorTotalMais2a3Anos_ProximoAno - ValorTotalMais2a3Anos_EsteAno;
    var ValorTotalMais2a3Anos_ProximoAnoFuturo = (ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais2a3Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais2a3Anos)) + ValorCarro) + ValorDespesasImportacao;
    var ValorTotalMais2a3Anos_DiferencaFuturo = ValorTotalMais2a3Anos_ProximoAno - ValorTotalMais2a3Anos_ProximoAnoFuturo;
    // 3 a 4 anos
    var ValorTotalMais3a4Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais3a4Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais3a4Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais3a4Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais3a4Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais3a4Anos_DiferencaAnos = ValorTotalMais3a4Anos_ProximoAno - ValorTotalMais3a4Anos_EsteAno;
    var ValorTotalMais3a4Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais3a4Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais3a4Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais3a4Anos_DiferencaFuturo = ValorTotalMais3a4Anos_ProximoAno - ValorTotalMais3a4Anos_ProximoAnoFuturo;
    // 4 a 5 anos
    var ValorTotalMais4a5Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais4a5Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais4a5Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais4a5Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais4a5Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais4a5Anos_DiferencaAnos = ValorTotalMais4a5Anos_ProximoAno - ValorTotalMais4a5Anos_EsteAno;
    var ValorTotalMais4a5Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais4a5Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais4a5Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais4a5Anos_DiferencaFuturo = ValorTotalMais4a5Anos_ProximoAno - ValorTotalMais4a5Anos_ProximoAnoFuturo;
    // 5 a 6 anos
    var ValorTotalMais5a6Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais5a6Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais5a6Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais5a6Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais5a6Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais5a6Anos_DiferencaAnos = ValorTotalMais5a6Anos_ProximoAno - ValorTotalMais5a6Anos_EsteAno;
    var ValorTotalMais5a6Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais5a6Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais5a6Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais5a6Anos_DiferencaFuturo = ValorTotalMais5a6Anos_ProximoAno - ValorTotalMais5a6Anos_ProximoAnoFuturo;
    // 6 a 7 anos
    var ValorTotalMais6a7Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais6a7Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais6a7Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais6a7Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais6a7Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais6a7Anos_DiferencaAnos = ValorTotalMais6a7Anos_ProximoAno - ValorTotalMais6a7Anos_EsteAno;
    var ValorTotalMais6a7Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais6a7Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais6a7Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais6a7Anos_DiferencaFuturo = ValorTotalMais6a7Anos_ProximoAno - ValorTotalMais6a7Anos_ProximoAnoFuturo;
    // 7 a 8 anos
    var ValorTotalMais7a8Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais7a8Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais7a8Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais7a8Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais7a8Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais7a8Anos_DiferencaAnos = ValorTotalMais7a8Anos_ProximoAno - ValorTotalMais7a8Anos_EsteAno;
    var ValorTotalMais7a8Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais7a8Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais7a8Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais7a8Anos_DiferencaFuturo = ValorTotalMais7a8Anos_ProximoAno - ValorTotalMais7a8Anos_ProximoAnoFuturo;
    // 8 a 9 anos
    var ValorTotalMais8a9Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais8a9Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais8a9Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais8a9Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais8a9Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais8a9Anos_DiferencaAnos = ValorTotalMais8a9Anos_ProximoAno - ValorTotalMais8a9Anos_EsteAno;
    var ValorTotalMais8a9Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais8a9Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais8a9Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais8a9Anos_DiferencaFuturo = ValorTotalMais8a9Anos_ProximoAno - ValorTotalMais8a9Anos_ProximoAnoFuturo;
    // 9 a 10 anos
    var ValorTotalMais9a10Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais9a10Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais9a10Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais9a10Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais9a10Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais9a10Anos_DiferencaAnos = ValorTotalMais9a10Anos_ProximoAno - ValorTotalMais9a10Anos_EsteAno;
    var ValorTotalMais9a10Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais9a10Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais9a10Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais9a10Anos_DiferencaFuturo = ValorTotalMais9a10Anos_ProximoAno - ValorTotalMais9a10Anos_ProximoAnoFuturo;
    // 10 a 11 anos
    var ValorTotalMais10a11Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais10a11Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais10a11Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais10a11Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais10a11Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais10a11Anos_DiferencaAnos = ValorTotalMais10a11Anos_ProximoAno - ValorTotalMais10a11Anos_EsteAno;
    var ValorTotalMais10a11Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais10a11Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais10a11Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais10a11Anos_DiferencaFuturo = ValorTotalMais10a11Anos_ProximoAno - ValorTotalMais10a11Anos_ProximoAnoFuturo;
    // 11 a 12 anos
    var ValorTotalMais11a12Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais11a12Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais11a12Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais11a12Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais11a12Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais11a12Anos_DiferencaAnos = ValorTotalMais11a12Anos_ProximoAno - ValorTotalMais11a12Anos_EsteAno;
    var ValorTotalMais11a12Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais11a12Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais11a12Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais11a12Anos_DiferencaFuturo = ValorTotalMais11a12Anos_ProximoAno - ValorTotalMais11a12Anos_ProximoAnoFuturo;
    // 12 a 13 anos
    var ValorTotalMais12a13Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais12a13Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais12a13Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais12a13Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais12a13Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais12a13Anos_DiferencaAnos = ValorTotalMais12a13Anos_ProximoAno - ValorTotalMais12a13Anos_EsteAno;
    var ValorTotalMais12a13Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais12a13Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais12a13Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais12a13Anos_DiferencaFuturo = ValorTotalMais12a13Anos_ProximoAno - ValorTotalMais12a13Anos_ProximoAnoFuturo;
    // 13 a 14 anos
    var ValorTotalMais13a14Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais13a14Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais13a14Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais13a14Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais13a14Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais13a14Anos_DiferencaAnos = ValorTotalMais13a14Anos_ProximoAno - ValorTotalMais13a14Anos_EsteAno;
    var ValorTotalMais13a14Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais13a14Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais13a14Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais13a14Anos_DiferencaFuturo = ValorTotalMais13a14Anos_ProximoAno - ValorTotalMais13a14Anos_ProximoAnoFuturo;
    // 14 a 15 anos
    var ValorTotalMais14a15Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais14a15Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais14a15Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais14a15Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais14a15Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais14a15Anos_DiferencaAnos = ValorTotalMais14a15Anos_ProximoAno - ValorTotalMais14a15Anos_EsteAno;
    var ValorTotalMais14a15Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais14a15Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais14a15Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais14a15Anos_DiferencaFuturo = ValorTotalMais14a15Anos_ProximoAno - ValorTotalMais14a15Anos_ProximoAnoFuturo;
    // mais de 15 anos
    var ValorTotalMais15Anos_EsteAno = ValorISVcm3_EsteAno - (ValorISVcm3_EsteAno * DescontoIdadeMais15Anos) + ValorISVCO2_EsteAno + ValorCarro + ValorDespesasImportacao;
    var ValorTotalMais15Anos_ProximoAno = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais15Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoCO2IdadeMais15Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais15Anos_DiferencaAnos = ValorTotalMais15Anos_ProximoAno - ValorTotalMais15Anos_EsteAno;
    var ValorTotalMais15Anos_ProximoAnoFuturo = ((ValorISVcm3_ProximoAno - (ValorISVcm3_ProximoAno * DescontoIdadeMais15Anos) + (ValorISVCO2_ProximoAno - Math.abs(ValorISVCO2_ProximoAno * DescontoIdadeMais15Anos)) + ValorCarro)) + ValorDespesasImportacao;
    var ValorTotalMais15Anos_DiferencaFuturo = ValorTotalMais15Anos_ProximoAno - ValorTotalMais15Anos_ProximoAnoFuturo;
// vamos apresentar os resultados na coluna à direita
    if (DadosISVcm3 > 100 && DadosISVCO2 > 10) {
        // vamos mostrar os dados da simulação para dar feedback ao utilizador de que está tudo a ser calculado com os dados que foram inseridos
        if (DadosCombustivel == "Gasoleo") {
            //se for a gasoleo
            carData = "Diesel " + Number(DadosISVcm3) + "cm3 " + Number(DadosISVCO2_ProximoAno) + "g/km CO2 " + DadosISVCO2WLTP + "Preço compra " + Number(ValorCarro) + "€";
        } else {
            //se for a gasolina
            carData = "Petrol " + Number(DadosISVcm3) + "cm3 " + Number(DadosISVCO2_ProximoAno) + "g/km CO2 " + DadosISVCO2WLTP + "Preço compra " + Number(ValorCarro) + "€";
        };

        // returns the year (four digits)
        var currentYear = currentTime.getFullYear();
        var carAge = currentYear - productionYear;

        switch(carAge){
            case 0:
            result = Number(Math.max(ValorISVMinimo,ValorTotalMais6Mesesa1Ano_EsteAno)).toFixed(2) + "€";
            case 1:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais1a2Anos_EsteAno)).toFixed(2) + "€";
            case 2:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais2a3Anos_EsteAno)).toFixed(2) + "€";
            case 3:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais3a4Anos_EsteAno)).toFixed(2) + "€";
            case 4:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais4a5Anos_EsteAno)).toFixed(2) + "€";
            case 5:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais5a6Anos_EsteAno)).toFixed(2) + "€";
            case 6:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais6a7Anos_EsteAno)).toFixed(2) + "€";
            case 7:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais7a8Anos_EsteAno)).toFixed(2) + "€";
            case 8:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais8a9Anos_EsteAno)).toFixed(2) + "€";
            case 9:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais9a10Anos_EsteAno)).toFixed(2) + "€";
            case 10:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais10a11Anos_EsteAno)).toFixed(2) + "€";
            case 11:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais11a12Anos_EsteAno)).toFixed(2) + "€";
            case 12:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais12a13Anos_EsteAno)).toFixed(2) + "€";
            case 13:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais13a14Anos_EsteAno)).toFixed(2) + "€";
            case 14:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais14a15Anos_EsteAno)).toFixed(2) + "€";
            default:
                result = Number(Math.max(ValorISVMinimo,ValorTotalMais15Anos_EsteAno)).toFixed(2) + "€";
        }
    }

    return result;
};