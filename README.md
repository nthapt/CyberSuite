## 🛡️ NTH Cyber Suite — Professional Security Toolkit

NTH Cyber Suite é um conjunto de ferramentas profissional focado em auditoria de segurança, monitoramento de rede, proteção de arquivos e análise de ameaças em tempo real em sistemas operacionais (incluindo suporte a macOS / Darwin, Linux e Windows).

## 📸 Interface da Aplicação
<img width="1067" height="664" alt="cyber" src="https://github.com/user-attachments/assets/f1c99f97-dfab-46b7-aeda-b024fc2970ee" />



+-------------------------------------------------------------------------------+
| NTH CYBER SUITE | Professional Security Toolkit                               |
| STATUS: ONLINE | OS: Darwin                                                    |
+-------------------------------------------------------------------------------+
| [📊 Dashboard] [📁 File Sentinel] [🌐 Network Defense]                       |
| [📝 Log Hunter] [🔍 Process Auditor] [🛡️ System Audit]                       |
+-------------------------------------------------------------------------------+
|                       SYSTEM LOG ANALYSIS & THREAT DETECTION                  |
|                                                                               |
|                            [ Analyze System Logs ]                            |
|                                                                               |
| -- LOG ANALYSIS RESULTS ----------------------------------------------------- |
| [16:53:02] | [INFO] Iniciando análise de logs de sistema...                   |
| ...                                                                           |
+-------------------------------------------------------------------------------+


# 💡 Recursos Principais (Modules)

O NTH Cyber Suite conta com módulos integrados para proteção e auditoria completa do ambiente:

# 📊 Dashboard

Visão geral do status de segurança do sistema em tempo real.

Telemetria e métricas de desempenho e integridade.

# 📁 File Sentinel

Monitoramento contínuo da integridade de arquivos críticos (File Integrity Monitoring - FIM).

Detecção preventiva contra alterações não autorizadas, ransomware e modificações maliciosas.

# 🌐 Network Defense

Análise de tráfego de rede e inspeção de conexões ativas.

Identificação de comportamentos anômalos e portas expostas.

# 📝 Log Hunter (Em destaque na captura)

Análise avançada de logs do sistema operacional (System Log Analysis & Threat Detection).

Varredura automatizada em busca de eventos suspeitos, tentativas de intrusão e falhas de autenticação.

# 🔍 Process Auditor

Mapeamento e auditoria de processos em execução no sistema.

Identificação de processos suspeitos, injeção de código ou consumo atípico de recursos.

# 🛡️  System Audit

Avaliação de conformidade (Hardening) do sistema operacional.

Verificação de configurações de segurança, permissões e vulnerabilidades conhecidas.

# 🚀 Tecnologias e Compatibilidade

Compatibilidade Multiplataforma: Projetado para funcionar com suporte nativo a ambientes Unix/Linux, macOS (Darwin) e Windows.

Interface: Gui amigável com suporte a modo escuro (Dark Mode) e navegação por abas.

Mecanismo de Logs: Parser interno rápido com suporte a filtragem e classificação por severidade ([INFO], [WARNING], [ERROR], [CRITICAL]).

# 🛠️ Como Executar

Pré-requisitos

Python 3.8+ (ou executável compilado do NTH Suite).

Permissões de administrador/root no sistema operacional para acesso completo aos logs e processos.

Passo a Passo

Clone o repositório:

git clone https://github.com/seu-usuario/nth-cyber-suite.git
cd nth-cyber-suite


Instale as dependências:

pip install -r requirements.txt


Inicie a aplicação:

# Em macOS / Linux (requer sudo para funções de auditoria de rede e sistema)
sudo python3 main.py

# Em Windows (executar terminal como Administrador)
python main.py


#📋 Exemplo de Uso (Log Hunter)

Abra a aplicação e navegue até a aba LOG HUNTER.

Clique no botão Analyze System Logs.

Acompanhe a execução e o relatório de ameaças gerado no painel em tempo real:

[16:53:02] | [INFO] Iniciando análise de logs de sistema...
[16:53:05] | [OK] Nenhum padrão de força bruta detectado nas últimas 24h.
[16:53:08] | [WARNING] Verificadas 3 tentativas de acesso malsucedidas.


📄 Licença

Este projeto é protegido sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

⚠️ Aviso de Uso Ético: Esta ferramenta foi desenvolvida para fins educacionais, de auditoria e defesa cibernética em sistemas autorizados.
