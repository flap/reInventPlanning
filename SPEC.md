# 📋 Especificação do Sistema — re:Invent Community Planner

> Sistema de planejamento de viagens e eventos para brasileiros participando de conferências internacionais de tecnologia.

---

## 1. Visão Geral

### 1.1 Problema

Brasileiros que participam de eventos internacionais de tecnologia (como AWS re:Invent, Google I/O, KubeCon, etc.) enfrentam uma combinação complexa de decisões: visto, passagem, hotel, agenda do evento, clima, bagagem, turismo e orçamento. As informações estão espalhadas em dezenas de fontes diferentes, em inglês, e sem considerar o contexto específico de quem vem do Brasil.

### 1.2 Solução

O **re:Invent Community Planner** é um sistema web que unifica todo o planejamento de viagem + evento em uma experiência guiada, com conteúdo curado em português, ferramentas interativas e timeline de preparação personalizada.

### 1.3 Público-Alvo

- Profissionais de tecnologia brasileiros (desenvolvedores, arquitetos, DevOps, gestores)
- Primeira viagem internacional ou primeira vez no evento
- Participantes recorrentes que querem otimizar o planejamento
- Empresas enviando colaboradores a conferências

### 1.4 Primeiro Destino/Evento

**AWS re:Invent 2026** — Las Vegas, Nevada, EUA (30 Nov – 4 Dez 2026)

O sistema é projetado para ser extensível a qualquer combinação destino + evento, mas o re:Invent serve como implementação de referência com conteúdo completo.

---

## 2. Princípios de Design

| Princípio | Descrição |
|-----------|-----------|
| **Content-first** | Conteúdo curado e opinativo, não genérico |
| **Mobile-friendly** | Funciona bem no celular durante a viagem |
| **Offline-capable** | Dados essenciais acessíveis sem internet |
| **Progressive** | Começa simples (markdown/HTML), evolui conforme demanda |
| **Localizado** | Português BR como idioma principal, perspectiva brasileira |
| **Actionable** | Cada informação leva a uma ação concreta |

---

## 3. Arquitetura do Sistema

### 3.1 Fase Atual (v1 — GitHub Pages)

```
┌─────────────────────────────────────────────────┐
│                GitHub Pages                       │
├─────────────────────────────────────────────────┤
│  index.html          → Landing page              │
│  guias/*.md          → Conteúdo estático         │
│  ferramenta/*.html   → Apps client-side          │
│                                                   │
│  Persistência: localStorage (browser)            │
│  Deploy: GitHub Actions (push → main)            │
└─────────────────────────────────────────────────┘
```

### 3.2 Fase Futura (v2 — App Progressivo)

```
┌───────────────┐     ┌──────────────────┐     ┌─────────────┐
│   Frontend    │────▶│   Backend API    │────▶│  Database   │
│   (PWA/SPA)  │◀────│  (Serverless)    │◀────│  (DynamoDB) │
└───────────────┘     └──────────────────┘     └─────────────┘
       │                       │
       │                       ▼
       │              ┌──────────────────┐
       │              │  Integrações     │
       │              │  - AWS Events API│
       │              │  - Google Flights│
       │              │  - Weather API   │
       │              └──────────────────┘
       ▼
┌───────────────┐
│  Service      │
│  Worker       │
│  (Offline)    │
└───────────────┘
```

---

## 4. Modelo de Dados (Conceitual)

### 4.1 Entidades Principais

```
Evento {
  id, nome, cidade, país, local_principal,
  data_inicio, data_fim, site_oficial,
  tipos_sessao[], venues[]
}

Destino {
  id, cidade, país, aeroporto_principal,
  fuso_horario, clima_periodo{},
  dicas_locais[], custos_referencia{}
}

Viagem (instância do usuário) {
  id, usuario_id, evento_id, destino_id,
  data_ida, data_volta, hotel,
  status_visto, status_passagem,
  checklist_progresso{}, orcamento{}
}

Sessao (do evento) {
  id, evento_id, codigo, tipo, nivel,
  titulo, descricao, venue, horario,
  reservada: boolean
}
```

---

## 5. Features do Sistema

Cada feature é derivada do conteúdo existente nos guias do projeto, expandida para um sistema interativo.

---

### Feature 1: Informações do Evento e Agenda

> Fonte: `guias/01-sobre-o-evento.md`

**Objetivo:** Apresentar o evento de forma clara, ajudar o usuário a entender a estrutura e montar sua agenda personalizada.

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F1.1 | Página de overview do evento (o que é, datas, local) | Alta |
| F1.2 | Catálogo de tipos de sessão com descrição e dicas | Alta |
| F1.3 | Níveis de profundidade (100–400) com recomendações por perfil | Média |
| F1.4 | Timeline de registro (quando se inscrever, quando reservar sessões) | Alta |
| F1.5 | Montador de agenda pessoal com sessões prioritárias + alternativas | Alta |
| F1.6 | Cronograma típico da semana (dia a dia) | Média |
| F1.7 | Dicas de primeira vez (checklist do que fazer antes/durante) | Alta |
| F1.8 | Mapa de venues com distâncias e tempos de deslocamento | Média |

**Conteúdo base já disponível:**
- Tipos de sessão (KEY, BLD, BOF, CHL, CON, DEM, GAM, LAB, WRK)
- Níveis de profundidade (100–400)
- Tipo de pass: Full Conference Pass apenas (Expo Pass descontinuado a partir de 2026)
- Cronograma típico da semana (domingo a sexta)
- 15+ dicas para primeira vez
- Links para app oficial, site e YouTube

---

### Feature 2: Hospedagem e Acomodação

> Fonte: `guias/02-hoteis-hospedagem.md`

**Objetivo:** Ajudar o usuário a escolher o melhor hotel para seu orçamento e perfil, considerando proximidade do evento.

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F2.1 | Comparativo de hotéis (preço, distância, nível, prós/contras) | Alta |
| F2.2 | Filtro por orçamento, proximidade e necessidades | Média |
| F2.3 | Mapa interativo com hotéis e venues do evento | Média |
| F2.4 | Calculadora de custo total (diária + resort fee + gorjetas) | Alta |
| F2.5 | Informações do sistema de shuttle gratuito (rotas, horários) | Alta |
| F2.6 | Dicas de reserva (quando, onde, política de cancelamento) | Média |
| F2.7 | Alertas de preço / links para booking | Baixa |

**Conteúdo base já disponível:**
- 8 hotéis catalogados com preço, distância e nível
- Sistema de shuttle (rotas, frequência, horários)
- Resort fees e gorjetas detalhadas
- Dicas de Wi-Fi, segurança e reserva
- Tabela comparativa completa

---

### Feature 3: Transporte e Documentação

> Fonte: `guias/03-voos-deslocamento.md`

**Objetivo:** Guiar o usuário em toda a logística de transporte: voo, visto, chip de dados e deslocamento local.

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F3.1 | Guia de voos do Brasil (conexões, companhias, tempo de viagem) | Alta |
| F3.2 | Dicas de compra de passagem (quando, como economizar) | Alta |
| F3.3 | Guia completo de visto americano B1/B2 (documentos, timeline) | Alta |
| F3.4 | Calculadora de fuso horário e jet lag | Baixa |
| F3.5 | Opções de transporte aeroporto → hotel (preços, tempos) | Alta |
| F3.6 | Guia de deslocamento durante o evento (shuttle, monorail, Uber) | Média |
| F3.7 | Comparativo de chips de dados / eSIM para EUA | Média |
| F3.8 | Checklist de documentação (passaporte, visto, seguro) | Alta |

**Conteúdo base já disponível:**
- 6 rotas de conexão do Brasil com companhias e tempos
- Guia completo de visto (DS-160, documentos, carta de convite)
- 4 opções de transporte aeroporto–hotel com preços
- Comparativo de chips (T-Mobile, AT&T, Google Fi, eSIMs)
- Programas de milhas recomendados
- Checklist completo de voo e chegada

---

### Feature 4: Preparação, Clima e Bagagem

> Fonte: `guias/04-clima-vestuario.md`

**Objetivo:** Preparar o usuário para as condições climáticas e montar uma mala eficiente.

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F4.1 | Informações climáticas do destino no período do evento | Alta |
| F4.2 | Guia de vestuário com princípio de camadas | Alta |
| F4.3 | Lista de mala interativa (check/uncheck itens) | Alta |
| F4.4 | Kit de saúde e remédios recomendados | Média |
| F4.5 | Dicas de hidratação e cuidados com clima seco | Média |
| F4.6 | Conteúdo da mochila do dia (essenciais para o evento) | Alta |
| F4.7 | Informações sobre adaptador de tomada e voltagem | Baixa |
| F4.8 | Dicas de seguro viagem (cobertura mínima, seguradoras) | Alta |

**Conteúdo base já disponível:**
- Temperaturas detalhadas por período do dia
- Lista completa de roupas para 7 dias
- Conteúdo da mochila do dia (12 itens)
- Kit de remédios (7 medicamentos com indicação)
- Dicas de hidratação, pele, pés e jet lag
- Lista de mala despachada vs. mão
- Informações de voltagem e adaptador

---

### Feature 5: Atividades, Gastronomia e Compras

> Fonte: `guias/05-turismo-compras.md`

**Objetivo:** Maximizar a experiência do viajante fora do evento — turismo, gastronomia e compras.

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F5.1 | Guia de atrações com filtro por tipo, preço e distância | Alta |
| F5.2 | Sugestões por janela de tempo (noite, sábado, intervalos) | Média |
| F5.3 | Guia de compras por perfil (luxo, outlet, acessível) | Média |
| F5.4 | Guia gastronômico com faixa de preço e tipo de cozinha | Média |
| F5.5 | Passeios além da Strip (Grand Canyon, Red Rock, Hoover Dam) | Baixa |
| F5.6 | Estimativa de custos por atividade | Média |
| F5.7 | Spots para fotos com localização | Baixa |
| F5.8 | Dicas financeiras (câmbio, IOF, sales tax, gorjetas) | Alta |

**Conteúdo base já disponível:**
- 10+ atrações na Strip (pagas e gratuitas)
- 6 shoppings/outlets com lojas listadas
- 12+ restaurantes categorizados por faixa de preço
- 4 passeios fora da Strip com distância e custo
- Tabela de preços médios (15 itens)
- 8 spots para fotos
- Dicas financeiras completas (câmbio, cartão, sales tax)

---

### Feature 6: Planejamento e Acompanhamento de Tarefas

> Fonte: `ferramenta/checklist.html`

**Objetivo:** Ferramenta interativa de checklist com progresso visual e persistência de dados.

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F6.1 | Checklist com 80+ itens organizados por categoria | Alta |
| F6.2 | Barra de progresso global em tempo real | Alta |
| F6.3 | Sistema de prioridades (Alta, Média, Baixa) | Média |
| F6.4 | Persistência de progresso (localStorage → futuro: conta) | Alta |
| F6.5 | Abas por categoria (Documentação, Hotel, Voo, Evento, Mala, Turismo) | Alta |
| F6.6 | Reset de progresso | Baixa |
| F6.7 | Exportar/compartilhar checklist | Baixa |
| F6.8 | Notificações/lembretes por prazo | Média |

**Implementação existente:**
- Checklist HTML completo e funcional (`ferramenta/checklist.html`)
- Design system AWS (cores, tipografia)
- 7 abas organizadas por categoria
- Progresso com localStorage
- UI responsiva

---

### Feature 7: Timeline de Preparação

> Fonte: `README.md` (seção Cronograma) + `guias/00-indice.md`

**Objetivo:** Visualização temporal do que fazer e quando, com marcos e prazos.

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F7.1 | Timeline visual com marcos de preparação (9 meses → evento) | Alta |
| F7.2 | Personalização por data do evento (calcula prazos automaticamente) | Média |
| F7.3 | Status de cada marco (pendente, em andamento, concluído) | Alta |
| F7.4 | Alertas de prazo próximo | Média |
| F7.5 | Integração com checklist (marcos ligados a tarefas) | Média |
| F7.6 | Visão de calendário mensal | Baixa |

**Conteúdo base já disponível:**
- Cronograma completo de 9 meses dividido em fases
- Marcos com ações específicas por período
- Priorização temporal clara

---

### Feature 8: Orçamento e Custos

> Fonte: Distribuída em vários guias (hotéis, voos, turismo, compras)

**Objetivo:** Consolidar todos os custos em um planejador financeiro da viagem, organizados por fase temporal.

**Organização por Fase:**

| Fase | Itens | Descrição |
|------|-------|-----------|
| 🗓️ Pré-evento | Passaporte, visto, passagem, hotel, ingresso, seguro, chip | Gastos meses antes da viagem |
| 🎪 Durante o evento | Resort fee, alimentação, transporte, turismo, extras | Gastos em Las Vegas |
| 📋 Pós-evento | Fatura cartão (IOF, câmbio) | Gastos na volta ao Brasil |

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F8.1 | Calculadora de orçamento total da viagem | Alta |
| F8.2 | Breakdown por categoria (passagem, hotel, evento, alimentação, turismo) | Alta |
| F8.3 | Conversão BRL/USD com taxa atualizada | Média |
| F8.4 | Comparativo de cenários (econômico, confortável, luxo) | Média |
| F8.5 | Inclusão de IOF, resort fees, sales tax | Alta |
| F8.6 | Dicas de economia por categoria | Média |
| F8.7 | Tracker de gastos durante a viagem | Baixa |
| F8.8 | Categorização temporal (pré/durante/pós-evento) | Alta |
| F8.9 | Custos de documentação (passaporte, visto) | Média |

**Dados de referência disponíveis:**
- Faixas de preço de 16 hotéis
- Custo de transporte (4 opções com preços)
- Tabela de preços médios (alimentação, bebidas, transporte)
- Sales tax Nevada (8,375%)
- Resort fees ($30–55/noite)
- Custos de passaporte (~R$257) e visto americano (~US$185+)

---

### Feature 9: Dicas Financeiras e Cartões

> Fonte: Contribuição da comunidade + issue #66

**Objetivo:** Guiar o viajante brasileiro na escolha do melhor meio de pagamento internacional, comparando IOF, câmbio e custos reais entre cartões de crédito, pré-pagos e soluções crypto.

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F9.1 | Guia de cartões de crédito internacionais emitidos no Brasil (IOF, cotação, alertas) | Alta |
| F9.2 | Guia de cartões pré-pagos internacionais com links (Wise, Nomad, C6, Inter, Nubank) | Alta |
| F9.3 | Guia de dólar digital / crypto-backed (ARQ, OKX) com IOF zero | Alta |
| F9.4 | Tabela comparativa de custo para USD 1.000 entre os 3 tipos | Alta |
| F9.5 | Dicas de DCA (compra antecipada de dólar) e segurança (clonagem) | Média |

**Conteúdo base:**
- IOF por tipo: 3,5% (crédito), 1,1% (pré-pago), 0% (crypto)
- Cotação: dólar turismo vs comercial vs spread crypto
- Recomendações com links: Wise, Nomad, Nubank Global, C6, Inter, ARQ, OKX
- Simulação comparativa com cotação de referência
- Dicas de segurança: clonagem, backup, notificações

---

---

### Feature 10: Tema Claro/Escuro (Dark Mode)

> Fonte: Solicitação de melhoria (UX / acessibilidade / conforto visual)

**Objetivo:** Permitir que o usuário alterne entre tema claro e escuro, com preferência persistida entre sessões, respeitando a preferência do sistema operacional como padrão inicial. Melhora o conforto visual em ambientes de baixa luminosidade (comum durante o evento e no voo) e reduz o consumo de bateria em telas OLED.

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F10.1 | Toggle de tema (claro ↔ escuro) acessível no header, ao lado do seletor de idioma | Alta |
| F10.2 | Persistência da preferência em `localStorage` (`tripevent:theme`) | Alta |
| F10.3 | Detecção automática de `prefers-color-scheme` como padrão inicial | Alta |
| F10.4 | Aplicação do tema em toda a estrutura (shell + views), sem "flash" de tema errado | Alta |
| F10.5 | Ícones/labels do toggle traduzidos nos 3 idiomas (☀️ Claro / 🌙 Escuro) | Alta |
| F10.6 | Transições suaves de cor ao alternar o tema | Média |
| F10.7 | Contraste adequado (WCAG AA) em ambos os temas | Média |

**Critérios de aceite:**

- Ao clicar no toggle, o app alterna imediatamente entre claro e escuro.
- A escolha persiste após recarregar a página e reabrir o navegador.
- Se o usuário nunca escolheu, o tema segue a preferência do sistema.
- O toggle exibe rótulo/ícone correto e traduzido nos 3 idiomas.
- Todas as superfícies principais (header, navegação, cards, footer) têm cor legível em ambos os temas.

**Decisão técnica:**

- Dark mode **controlado por classe** (`.dark` no elemento `<html>`), não por `prefers-color-scheme` puro — permite toggle manual sobrepondo o sistema.
- No Tailwind CSS v4 (CSS-first), habilitado via `@custom-variant dark`.
- Estado reativo compartilhado via composable `useTheme` (mesmo padrão do `useI18n`), com persistência em `localStorage`.

---

### Feature 11: Área Logada e Plano Salvo na Nuvem

> Fonte: Solicitação de evolução — introduz contas de usuário (Fase 3)

**Objetivo:** Permitir que o usuário crie uma conta, faça login e salve seu planejamento (checklist, orçamento, viagem, preferências) na nuvem, sincronizado entre dispositivos. Habilita as Features 12 e 13, que dependem de identidade autenticada.

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F11.1 | Cadastro e login de usuário (email + senha) via Amazon Cognito | Alta |
| F11.2 | Área logada (rotas protegidas) acessível apenas após autenticação | Alta |
| F11.3 | Salvar plano do usuário na nuvem (checklist, orçamento, viagem) | Alta |
| F11.4 | Sincronização localStorage ↔ nuvem com resolução de conflito (last-write-wins por timestamp) | Alta |
| F11.5 | Perfil do usuário (nome de exibição, avatar/emoji, idioma preferido) | Média |
| F11.6 | Logout e sessão persistente (token JWT com expiração) | Alta |
| F11.7 | Recuperação de senha (fluxo Cognito) | Média |
| F11.8 | Exclusão de conta e de todos os dados associados (LGPD/GDPR — direito ao esquecimento) | Alta |
| F11.9 | Uso anônimo continua funcionando (login é opcional; sem login, dados só locais) | Alta |

**Critérios de aceite:**

- Um visitante sem conta continua usando o app 100% com dados locais (nenhuma regressão da Fase 1).
- Após login, o plano local é migrado/sincronizado para a nuvem na primeira sessão.
- Ao reabrir em outro dispositivo e logar, o plano salvo é recuperado.
- Em conflito entre local e nuvem, prevalece a versão com timestamp mais recente.
- Rotas da área logada (Features 12 e 13) redirecionam para login se não autenticado.
- A exclusão de conta remove o perfil e todos os registros de plano e localização do usuário.

---

### Feature 12: Compartilhamento de Localização (Opt-in, Revogável, Expirável)

> Fonte: Solicitação de evolução — recurso social da área logada (Fase 3). Depende da Feature 11.

**Objetivo:** Permitir que usuários **logados** compartilhem, de forma **voluntária e reversível**, onde estão — seja por **local do re:Invent selecionado em um combo box** (padrão) ou por **localização GPS precisa** (opt-in adicional, com expiração automática). Visível apenas dentro da área logada. A **visualização é não-recíproca**: qualquer usuário logado pode ver quem está compartilhando, mesmo sem compartilhar; porém aparecer na lista continua sendo **opt-in** (ninguém é listado sem ter escolhido compartilhar).

**Modelo de privacidade (regras invioláveis):**

- **Opt-in por padrão desligado:** o usuário é **invisível** (não aparece na lista) até escolher explicitamente compartilhar.
- **Local por combo box é o modo padrão** (coarse): ex. "Venetian – Expo Hall". Não expõe coordenadas.
- **GPS preciso é opt-in adicional e expira automaticamente** (ex.: compartilhar por 1h/2h/4h), voltando a "desligado". Ao compartilhar por GPS, é oferecido um **link para o Google Maps** com a posição.
- **Revogável instantaneamente:** um toque para parar de compartilhar / ficar invisível.
- **Visibilidade não-recíproca (requer login):** qualquer usuário autenticado pode ver a lista de quem está compartilhando, mesmo sem compartilhar a própria localização. O requisito de estar na área logada se mantém.
- **Sem rastreamento silencioso:** nenhum usuário que não optou por compartilhar pode ser visualizado por outros (a mudança é do lado de quem vê, não de quem é visto).
- **Retenção mínima:** registros de localização expiram no servidor via TTL; GPS preciso tem expiração curta.

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F12.1 | Toggle "Compartilhar minha localização" (padrão: desligado) | Alta |
| F12.2 | Seleção de local via combo box com locais oficiais do re:Invent (venues/salas) | Alta |
| F12.3 | Opção adicional de GPS preciso com seletor de duração (1h/2h/4h) e expiração automática | Alta |
| F12.4 | Botão "Parar de compartilhar" (revogação imediata) | Alta |
| F12.5 | Consentimento explícito antes do primeiro compartilhamento (modal com política) | Alta |
| F12.6 | Visualização não-recíproca: qualquer logado vê a lista de quem está compartilhando | Alta |
| F12.7 | Expiração automática do registro de localização (TTL no servidor) | Alta |
| F12.8 | Indicador visível de "você está compartilhando agora" persistente na UI | Alta |
| F12.9 | Textos de consentimento e rótulos traduzidos nos 3 idiomas (PT/EN/ES) | Alta |
| F12.10 | Link para o Google Maps na posição GPS compartilhada por um peer | Média |

**Critérios de aceite:**

- Ao entrar na área logada pela primeira vez, o usuário **não** está compartilhando.
- Compartilhar exige aceite explícito de consentimento na primeira vez.
- Compartilhar por combo box nunca envia coordenadas GPS.
- Ao escolher GPS preciso, o registro expira sozinho ao fim da duração escolhida.
- Ao desligar o toggle, o usuário deixa de aparecer para os demais imediatamente.
- Um usuário logado pode ver a lista de quem está compartilhando mesmo sem compartilhar (não-recíproco); porém ninguém aparece na lista sem ter optado por compartilhar.
- Enquanto compartilha, há um indicador claro e sempre visível de que o compartilhamento está ativo.

---

### Feature 13: findPeople — Encontrar Peers para Meetups (Happy Hours e Talks)

> Fonte: Solicitação de evolução — recurso social da área logada (Fase 3). Depende das Features 11 e 12.

**Objetivo:** Ajudar usuários **logados** a se encontrarem para happy hours e talks, mostrando quem está compartilhando localização (via combo box ou GPS opt-in) e onde. Qualquer usuário logado pode ver a lista (não-recíproco); aparecer nela continua sendo opt-in (Feature 12).

**Funcionalidades:**

| ID | Funcionalidade | Prioridade |
|----|---------------|------------|
| F13.1 | Lista/mapa de peers que estão compartilhando localização no momento | Alta |
| F13.2 | Filtro por local (venue/sala do re:Invent) | Média |
| F13.3 | Agrupamento por local ("5 pessoas no Expo Hall agora") | Média |
| F13.4 | Códigos de "crew" opcionais: compartilhar um código com um grupo para se ver mutuamente | Média |
| F13.5 | Status/intenção opcional ("indo ao happy hour X", "na talk Y") — texto curto opt-in | Baixa |
| F13.6 | Atualização quase em tempo real da lista (polling ou WebSocket) | Média |
| F13.7 | Visualização não-recíproca (qualquer logado vê) + opt-in para quem é listado (Feature 12) | Alta |
| F13.8 | Destaque especial (ícone de pimenta 🌶️) para um usuário específico, ordenado no topo da lista | Baixa |

**Critérios de aceite:**

- findPeople só é acessível na área logada.
- Só aparecem peers que estão ativamente compartilhando; quem parou some da lista.
- Qualquer usuário logado vê os peers, mesmo sem compartilhar a própria localização (não-recíproco).
- Crew codes (quando usados) restringem a visibilidade ao grupo com o código, mantendo opt-in.
- Nenhum dado de localização de não-participantes é exibido em nenhuma circunstância.
- Peers que compartilham por GPS exibem um link para o Google Maps com a posição.
- O destaque 🌶️ é derivado **no servidor** (flag `isPepper`) comparando o email do perfil com o email-alvo configurado; o **email nunca é exposto** na listagem de peers (minimização de dados — ADR-011).

---

O sistema é projetado para suportar múltiplos destinos e eventos. O re:Invent é a **implementação de referência** que define o template para futuros destinos.

### 6.1 Template de Evento

Cada novo evento adicionado ao sistema deve incluir:

```yaml
evento:
  nome: "AWS re:Invent 2026"
  tipo: "conferência técnica"
  cidade: "Las Vegas"
  pais: "EUA"
  periodo: "30 Nov – 4 Dez 2026"
  
  conteudo_obrigatorio:
    - sobre_o_evento      # O que é, estrutura, registro
    - hospedagem          # Hotéis, preços, localização
    - transporte          # Voos, visto, deslocamento local
    - clima_vestuario     # Clima, o que vestir, saúde
    - turismo_compras     # O que fazer fora do evento
    - checklist           # Tarefas de preparação
    - timeline            # Cronograma temporal
    - orcamento           # Custos e planejamento financeiro

  conteudo_opcional:
    - networking          # Dicas de networking
    - certificacoes       # Provas/labs durante o evento
    - pos_evento          # Aproveitamento pós-conferência
```

### 6.2 Eventos Futuros Candidatos

| Evento | Cidade | Período | Público |
|--------|--------|---------|---------|
| AWS re:Invent | Las Vegas, EUA | Dezembro | Cloud/DevOps |
| Google I/O | Mountain View, EUA | Maio | Desenvolvimento |
| KubeCon NA | Variável, EUA | Outubro-Novembro | Kubernetes/Cloud Native |
| Microsoft Build | Seattle, EUA | Maio | Microsoft/.NET |
| Web Summit | Lisboa, Portugal | Novembro | Tech geral |
| AWS Summit SP | São Paulo, BR | Variável | Cloud (local) |
| re:Inforce | Integrado ao re:Invent (desde 2026) | Dezembro (dia dedicado) | Segurança |

### 6.3 Dados Compartilhados entre Eventos

Quando múltiplos eventos ocorrem na mesma cidade, os dados de destino são reutilizados:

- **Las Vegas:** Hotéis, clima dezembro, turismo, compras, transporte
- **São Paulo:** Não precisa de visto/voo internacional, foco no evento
- **Seattle:** Clima maio, hotéis, transporte, turismo local

---

## 7. Roadmap de Implementação

### Fase 1 — MVP Estático (✅ Atual)

**Status:** Implementado e publicado

| Entrega | Status |
|---------|--------|
| Guias em markdown (5 guias completos) | ✅ Pronto |
| Checklist interativo HTML | ✅ Pronto |
| Landing page (index.html) | ✅ Pronto |
| Deploy automático GitHub Pages | ✅ Pronto |
| Design system AWS (cores, tipografia) | ✅ Pronto |

**Stack:** HTML, CSS, JavaScript vanilla, GitHub Pages

---

### Fase 2 — App Interativo (Próximo)

**Objetivo:** Transformar o conteúdo estático em experiência interativa e personalizada.

| Entrega | Prioridade | Estimativa |
|---------|-----------|------------|
| Calculadora de orçamento interativa | Alta | 2 semanas |
| Timeline visual de preparação | Alta | 1 semana |
| Mapa interativo de venues e hotéis | Média | 2 semanas |
| Filtro/comparador de hotéis | Média | 1 semana |
| PWA com suporte offline | Média | 1 semana |
| Montador de agenda de sessões | Alta | 2 semanas |
| Tema claro/escuro (Dark Mode) — Feature 10 | Alta | 3 dias |

**Stack sugerida:** HTML/CSS/JS (vanilla ou framework leve), Service Worker para offline

---

### Fase 3 — Multi-evento e Personalização

**Objetivo:** Expandir para múltiplos eventos e adicionar personalização por usuário.

| Entrega | Prioridade | Estimativa |
|---------|-----------|------------|
| Sistema de templates para novos eventos | Alta | 3 semanas |
| Segundo evento implementado (ex: KubeCon) | Alta | 2 semanas |
| Conta de usuário + área logada + plano na nuvem (Feature 11) | Alta | 3 semanas |
| Compartilhamento de localização opt-in (Feature 12) | Alta | 2 semanas |
| findPeople — meetup finder (Feature 13) | Média | 2 semanas |
| Notificações de prazo (email/push) | Média | 2 semanas |
| Compartilhamento de planejamento | Baixa | 1 semana |
| Modo colaborativo (viagem em grupo) | Baixa | 3 semanas |

**Stack sugerida:** Backend serverless (Lambda + DynamoDB), autenticação (Cognito)

---

### Fase 4 — Integrações e Inteligência

**Objetivo:** Conectar com APIs externas e adicionar recomendações inteligentes.

| Entrega | Prioridade | Estimativa |
|---------|-----------|------------|
| Integração com API de clima (previsão tempo real) | Média | 1 semana |
| Alerta de preço de passagens (Google Flights) | Alta | 2 semanas |
| Câmbio em tempo real (BRL/USD) | Média | 3 dias |
| Recomendações de sessões por perfil | Baixa | 3 semanas |
| Integração com app AWS Events (agenda) | Baixa | 2 semanas |
| Assistente IA para perguntas sobre o evento | Baixa | 3 semanas |

---

## 8. Métricas de Sucesso

### 8.1 Métricas de Produto

| Métrica | Meta (v1) | Meta (v2) |
|---------|-----------|-----------|
| Usuários únicos/mês | 500 | 5.000 |
| Tempo médio na página | > 3 min | > 5 min |
| Checklist completion rate | > 30% | > 50% |
| Retorno (usuários recorrentes) | > 20% | > 40% |
| NPS (satisfação) | > 40 | > 60 |

### 8.2 Métricas de Conteúdo

| Métrica | Meta |
|---------|------|
| Guias completos por evento | ≥ 5 |
| Itens no checklist | ≥ 80 |
| Acurácia de preços (atualização) | Trimestral |
| Cobertura de dúvidas comuns | > 90% das perguntas FAQ |

---

## 9. Decisões Técnicas e Restrições

### 9.1 Decisões Tomadas

| Decisão | Justificativa |
|---------|---------------|
| GitHub Pages como hosting | Gratuito, simples, integrado ao workflow de contribuição |
| Conteúdo em Markdown | Fácil de editar, versionável, renderizável em qualquer plataforma |
| Ferramentas em HTML/JS vanilla | Sem dependências, funciona offline, carrega rápido |
| localStorage para persistência | Zero infraestrutura backend na v1 |
| Português BR como idioma principal | Público-alvo são brasileiros; conteúdo em português é diferencial |
| Deploy automático via push → main | Reduz fricção para contribuições |

### 9.2 Restrições

| Restrição | Impacto | Mitigação |
|-----------|---------|-----------|
| Sem backend (v1) | Sem sincronização entre dispositivos | Evolução para PWA com sync na v2 |
| Conteúdo manual | Preços e informações podem desatualizar | Revisão trimestral + contribuições da comunidade |
| GitHub Pages limitações | Sem SSR, sem API routes | Suficiente para v1/v2, migrar se necessário |
| Sem autenticação (v1) | Dados apenas locais | Cognito na fase 3 |

### 9.3 Stack Técnica por Fase

| Fase | Frontend | Backend | Dados | Hosting |
|------|----------|---------|-------|---------|
| v1 (atual) | HTML/CSS/JS vanilla | — | localStorage | GitHub Pages |
| v2 | HTML/CSS/JS + Service Worker | — | localStorage + IndexedDB | GitHub Pages |
| v3 | SPA (React/Astro) | Lambda + API Gateway | DynamoDB | CloudFront + S3 |
| v4 | SPA + integrações | Lambda + Step Functions | DynamoDB + cache | CloudFront + S3 |

---

## 10. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Informações desatualizadas (preços, datas) | Alta | Médio | Revisão trimestral, versionamento de datas, avisos de "última atualização" |
| Baixa adoção | Média | Alto | SEO, divulgação em comunidades AWS BR, conteúdo de qualidade |
| Escopo muito amplo (multi-evento) | Média | Médio | Template bem definido, implementar um evento por vez |
| Dependência de contribuições voluntárias | Alta | Médio | Manter core mínimo viável, automações para reduzir trabalho manual |
| Mudanças no evento (venues, estrutura) | Baixa | Baixo | Conteúdo modular, fácil de atualizar seções específicas |

---

## 11. Apêndice — Mapeamento Conteúdo Existente → Features

| Arquivo Existente | Feature(s) Mapeada(s) | Status do Conteúdo |
|-------------------|----------------------|-------------------|
| `guias/01-sobre-o-evento.md` | F1 (Evento e Agenda) | ✅ Completo |
| `guias/02-hoteis-hospedagem.md` | F2 (Hospedagem) | ✅ Completo |
| `guias/03-voos-deslocamento.md` | F3 (Transporte e Documentação) | ✅ Completo |
| `guias/04-clima-vestuario.md` | F4 (Clima e Bagagem) | ✅ Completo |
| `guias/05-turismo-compras.md` | F5 (Turismo e Compras) | ✅ Completo |
| `ferramenta/checklist.html` | F6 (Checklist) | ✅ Implementado |
| `README.md` (cronograma) | F7 (Timeline) | ✅ Conteúdo pronto |
| Distribuído (preços em vários guias) | F8 (Orçamento) | 🟡 Dados disponíveis, ferramenta pendente |
| `index.html` | Landing page / Navegação | ✅ Implementado |
| `.github/workflows/deploy-pages.yml` | Infraestrutura CI/CD | ✅ Configurado |

---

## 12. Próximos Passos Imediatos

1. **Validar esta especificação** com stakeholders e comunidade
2. **Priorizar entregas da Fase 2** — selecionar 2-3 features para sprint inicial
3. **Criar issues no GitHub** para cada feature priorizada
4. **Implementar calculadora de orçamento** (Feature 8) — maior gap atual
5. **Implementar timeline visual** (Feature 7) — alto valor, baixo esforço
6. **Definir template formal** para novos eventos (seção 6.1)

---

*Documento criado em: Julho 2026*
*Última atualização: 12/07/2026*
*Versão: 1.0*
