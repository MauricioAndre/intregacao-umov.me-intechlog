entregas="""
select

 

scheduletype,serviceLocal,team,teamExecution,agent,

 

alternativeIdentifier,dateA,TO_CHAR(hourA,'HH:MI')AS hourA,executionForecastEndDate,

 

TO_CHAR(executionForecastEndTime,'HH:MI')AS executionForecastEndTime,observation,situation,customfield1,customfield2,

 

tar_veiculo,tar_embarcador,STRING_AGG(listas_ctes,'/') as listas_ctes

 

from

 

(

 

SELECT 'entrega'::TEXT AS scheduleType

 

 

       ,FNC_FORMATA_CNPJCPFCOD(conhecimento.destinatario) AS serviceLocal

 

 

       ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque.cnpjcpfcodigoveiculo),1,10) AS team

 

 

       ,0::integer AS teamExecution

 

 

       ,FNC_FORMATA_CNPJCPFCOD(programacaoembarque.motorista) AS agent

 

 

       ,CONCAT(programacaoembarque.grupo

 

 

               ||'-'||programacaoembarque.empresa

 

 

               ||'-'||programacaoembarque.diferenciadornumero

 

 

               ||'-'||programacaoembarque.numero

 

 

               ||'-'||FNC_FORMATA_CNPJCPFCOD(conhecimento.destinatario)

 

 

               ||'-'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)) AS alternativeIdentifier

 

 

       ,programacaoembarque.dtemissao::DATE AS dateA

 

 

       ,(CASE EXTRACT( DOW FROM programacaoembarque.dtemissao)

 

 

            WHEN 0 THEN cadastro_vinculo_clienteapoiologistico.hrinicialcoletarreceberdomingo

 

 

            WHEN 1 THEN cadastro_vinculo_clienteapoiologistico.hrinicialcoletarrecebersegundafeira

 

 

            WHEN 2 THEN cadastro_vinculo_clienteapoiologistico.hrinicialcoletarrecebertercafeira

 

 

            WHEN 3 THEN cadastro_vinculo_clienteapoiologistico.hrinicialcoletarreceberquartafeira

 

 

            WHEN 4 THEN cadastro_vinculo_clienteapoiologistico.hrinicialcoletarreceberquintafeira

 

 

            WHEN 5 THEN cadastro_vinculo_clienteapoiologistico.hrinicialcoletarrecebersextafeira

 

 

            WHEN 6 THEN cadastro_vinculo_clienteapoiologistico.hrinicialcoletarrecebersabado

 

 

      END) AS hourA

 

 

       ,programacaoembarque.dtemissao::DATE AS executionForecastEndDate

 

 

       ,(CASE EXTRACT( DOW FROM programacaoembarque.dtemissao)

 

 

            WHEN 0 THEN cadastro_vinculo_clienteapoiologistico.hrfinalcoletarreceberdomingo

 

 

            WHEN 1 THEN cadastro_vinculo_clienteapoiologistico.hrfinalcoletarrecebersegundafeira

 

 

            WHEN 2 THEN cadastro_vinculo_clienteapoiologistico.hrfinalcoletarrecebertercafeira

 

 

            WHEN 3 THEN cadastro_vinculo_clienteapoiologistico.hrfinalcoletarreceberquartafeira

 

 

            WHEN 4 THEN cadastro_vinculo_clienteapoiologistico.hrfinalcoletarreceberquintafeira

 

 

            WHEN 5 THEN cadastro_vinculo_clienteapoiologistico.hrfinalcoletarrecebersextafeira

 

 

            WHEN 6 THEN cadastro_vinculo_clienteapoiologistico.hrfinalcoletarrecebersabado

 

 

      END) AS executionForecastEndTime

 

 

       ,CONCAT('Remetente:'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)

 

 

           ||' '||'Quantidade:'||programacaoembarque.quantidade

 

 

           ||' '||'Peso:'||programacaoembarque.peso

 

 

           ||' '||'P.E:'||programacaoembarque.grupo

 

 

               ||'-'||programacaoembarque.empresa

 

 

               ||'-'||programacaoembarque.diferenciadornumero

 

 

               ||'-'||programacaoembarque.numero

 

 

          ) AS observation

 

 

        ,40::integer AS situation

 

 

        ,CONCAT(programacaoembarque.grupo

 

 

               ||'-'||programacaoembarque.empresa

 

 

               ||'-'||programacaoembarque.filialdocumentoorigem

 

 

               ||'-'||programacaoembarque.unidadedocumentoorigem

 

 

               ||'-'||programacaoembarque.diferenciadornumerodocumentoorigem

 

 

               ||'-'||programacaoembarque.seriedocumentoorigem

 

 

               ||'-'||programacaoembarque.numerodocumentoorigem

 

 

           ) AS customField1

 

 

        ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10) AS customField2

 

 

        ,programacaoembarque.veiculo AS tar_veiculo

 

 

        ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10) AS tar_embarcador

 

 

        ,conhecimento.chaveacessocte AS listas_ctes

 

 

FROM programacaoembarque

 

 

LEFT JOIN programacaoembarque_composicao

 

 

    ON  programacaoembarque.grupo = programacaoembarque_composicao.grupo

 

 

    AND programacaoembarque.empresa = programacaoembarque_composicao.empresa

 

 

    AND programacaoembarque.diferenciadornumero = programacaoembarque_composicao.diferenciadornumero

 

 

    AND programacaoembarque.numero = programacaoembarque_composicao.numero

 

 

LEFT JOIN cadastro_vinculo_clienteapoiologistico

 

 

    ON programacaoembarque_composicao.cnpjcpfcodigoclientecoletaentrega = cadastro_vinculo_clienteapoiologistico.cnpjcpfcodigo

 

 

LEFT JOIN conhecimento

 

 

    ON  programacaoembarque_composicao.grupo = conhecimento.grupo

 

 

    AND programacaoembarque_composicao.empresa = conhecimento.empresa

 

 

    AND programacaoembarque_composicao.filialdocumento = conhecimento.filial

 

 

    AND programacaoembarque_composicao.unidadedocumento = conhecimento.unidade

 

 

    AND programacaoembarque_composicao.diferenciadornumerodocumento = conhecimento.diferenciadornumero

 

 

    AND programacaoembarque_composicao.seriedocumento = conhecimento.serie

 

 

    AND programacaoembarque_composicao.numerodocumento = conhecimento.numero

 

 

 WHERE programacaoembarque.numero < 1000000 

 AND programacaoembarque.unidade = 1

 --and programacaoembarque.numero=56858

 AND programacaoembarque.dtemissao::date = now()::date

 

 

) as base

 where base.houra is not null

group by scheduletype,serviceLocal,team,teamExecution,agent,

 

alternativeIdentifier,dateA,hourA,executionForecastEndDate,

 

executionForecastEndTime,observation,situation,customfield1,customfield2,

 

tar_veiculo,tar_embarcador
    """



items=""" 

select



description

,alternativeIdentifier

,schedule

from

 

(

 

SELECT   'notas_fiscais'::TEXT AS subGroup

 

     ,CONCAT('CT-e'::TEXT||' '||conhecimento.numero) AS description

 

        ,conhecimento.chaveacessocte AS alternativeIdentifier

 

        ,CONCAT(programacaoembarque.grupo

               ||'-'||programacaoembarque.empresa

               ||'-'||programacaoembarque.diferenciadornumero

               ||'-'||programacaoembarque.numero

               ||'-'||FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoclientecoletaentrega)

               ||'-'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)) AS schedule

 

 

FROM programacaoembarque

 

 

LEFT JOIN programacaoembarque_composicao

 

 

    ON  programacaoembarque.grupo = programacaoembarque_composicao.grupo

 

 

    AND programacaoembarque.empresa = programacaoembarque_composicao.empresa

 

 

    AND programacaoembarque.diferenciadornumero = programacaoembarque_composicao.diferenciadornumero

 

 

    AND programacaoembarque.numero = programacaoembarque_composicao.numero

 

 

LEFT JOIN cadastro_vinculo_clienteapoiologistico

 

 

    ON programacaoembarque_composicao.cnpjcpfcodigoclientecoletaentrega = cadastro_vinculo_clienteapoiologistico.cnpjcpfcodigo

 

 

LEFT JOIN conhecimento

 

 

    ON  programacaoembarque_composicao.grupo = conhecimento.grupo

 

 

    AND programacaoembarque_composicao.empresa = conhecimento.empresa

 

 

    AND programacaoembarque_composicao.filialdocumento = conhecimento.filial

 

 

    AND programacaoembarque_composicao.unidadedocumento = conhecimento.unidade

 

 

    AND programacaoembarque_composicao.diferenciadornumerodocumento = conhecimento.diferenciadornumero

 

 

    AND programacaoembarque_composicao.seriedocumento = conhecimento.serie

 

 

    AND programacaoembarque_composicao.numerodocumento = conhecimento.numero

 

 

 WHERE programacaoembarque.numero < 1000000 

 
    AND programacaoembarque.dtemissao::date = now()::date

 

 

) as base

 

group by



description

,alternativeIdentifier

,schedule

"""