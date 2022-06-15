Grupo

- Arthur Gomes de Lima
- Gustavo Rocha Figueiredo
- Igor Oliveira Valente da Silveira

Explicação do sistema

- Esse trabalho visa criar um software que simulará uma dinâmica em um hospital fictício, gerenciando equipes médicas e de enfermagem de acordo com a necessidade. Dessa forma, o hospital será dividido em blocos com um número específico de leitos. Cada um desses leitos terá uma gravidade do paciente associado a ele. Exemplo: leve, moderado, grave, gravíssimo ou leito vazio. O sistema irá alocar uma quantidade específica de profissionais por bloco de acordo com os leitos associados a esses blocos. Para que o sistema entenda quantas pessoas da equipe médica ou de enfermagem poderiam alocar, iremos criar uma regra (exemplo: gravíssimo exige um profissional por leito, grave um profissional para dois leitos, moderado um profissional para três leitos e leve um profissional para cada quatro leitos). Dessa forma, os profissionais serão alocados de acordo com a gravidade e necessidade dos leitos de cada bloco. Em casos de emergência
(pacientes em estado gravíssimo), o sistema deverá parar toda e qualquer alocação e focar nesses pacientes, para garantir o atendimento mais rápido possível. Vale ressaltar que existirá uma quantidade limitada de funcionários, o que pode causar uma falta de equipe médica no ambiente. Assim, o sistema também deverá alocar as equipes de forma mais eficaz possível, privilegiando os pacientes graves e gravíssimos.