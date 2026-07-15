# Steering: re:Invent Community Planner — Fluxo de Atendimento de Issues

## Objetivo

Definir o fluxo padrão para análise, aprovação e implementação de issues neste projeto, garantindo qualidade, consistência e alinhamento com os requisitos e design existentes.

---

## Fluxo 1: Issues do tipo TIP (Dica da Comunidade)

Issues criadas por usuários externos usando o template "💡 Dica da Comunidade (TIP)".

### Etapas

1. **Analisar a dica**
   - Ler o conteúdo da issue e entender a sugestão
   - Verificar a categoria e edição do re:Invent mencionada
   - Avaliar se a informação é precisa e verificável

2. **Verificar impacto nos requisitos (SPEC.md)**
   - A dica se encaixa em alguma feature existente?
   - Conflita com informações já publicadas no app?
   - Requer criação de nova feature ou seção?

3. **Verificar impacto no design (DESIGN.md)**
   - A dica cabe em uma view existente?
   - Precisa de novo componente ou dados adicionais?
   - Impacta a estrutura de navegação?

4. **Decisão**
   - ✅ **Aprovada:** Sugerir implementação indicando onde a dica será incorporada (view, seção, dados). Creditar o autor.
   - ❌ **Recusada:** Comentar na issue com motivo claro (informação imprecisa, fora do escopo, duplicada, desatualizada). Agradecer pela contribuição.

5. **Se aprovada — Implementar**
   - Seguir o Fluxo de Implementação (abaixo)
   - Adicionar entrada na release-notes.json com type "community"
   - Fechar a issue com comentário documentando o que foi implementado

---

## Fluxo 2: Demais Issues (Features, Bugs, Melhorias)

Issues de funcionalidades, correções ou melhorias criadas pelos mantenedores ou colaboradores.

### Etapas

1. **Analisar a issue**
   - Entender o problema ou funcionalidade solicitada
   - Verificar se já existe issue duplicada ou relacionada

2. **Confrontar com requisitos (SPEC.md)**
   - A issue está alinhada com a visão do produto?
   - Faz sentido no contexto do público-alvo (brasileiros indo ao re:Invent)?
   - Se necessário, sugerir atualização na SPEC.md (novas features, novos dados)

3. **Confrontar com design (DESIGN.md)**
   - A implementação se encaixa na arquitetura existente?
   - Precisa de novos componentes, stores, rotas ou dados?
   - Se necessário, sugerir atualização no DESIGN.md

4. **Decisão**
   - ✅ **Implementar:** Seguir o Fluxo de Implementação
   - 🔄 **Precisa de mais contexto:** Pedir clarificação na issue
   - ❌ **Recusar:** Comentar com motivo (fora do escopo, conflita com arquitetura, etc.)

---

## Fluxo de Implementação (Padrão para Ambos)

### Pré-implementação

1. **Ler arquivos relevantes** antes de alterar qualquer código
2. **Verificar SPEC.md** — atualizar se necessário (nova feature, novo dado)
3. **Verificar DESIGN.md** — atualizar se necessário (nova view, novo componente)
4. **Criar issue no GitHub** se ainda não existir (com labels adequados)

### Implementação

5. **Seguir padrões existentes do projeto:**
   - Vue.js 3 + TypeScript + Composition API (`<script setup>`)
   - Tailwind CSS com classes do design system (aws-dark, aws-orange, rounded-xl, shadow-sm)
   - Dados inline com objeto `{pt, en, es}` ou i18n via `useI18n()`
   - JSON em `src/data/` para dados estruturados
   - Pinia para estado global

6. **Compatibilidade obrigatória com os 3 idiomas:**
   - Português (PT-BR) — idioma primário
   - English (EN-US)
   - Español (ES-LATAM)
   - Todo texto visível ao usuário deve existir nos 3 idiomas
   - Atualizar `src/locales/pt.ts`, `en.ts`, `es.ts` quando usar chaves i18n

7. **Segurança (Zero Trust):**
   - Links externos sempre com `target="_blank" rel="noopener noreferrer"`
   - Não confiar em dados de localStorage sem validação/migração
   - Input sanitization em formulários
   - Não expor dados sensíveis no frontend

8. **Well-Architected Framework:**
   - Performance: lazy loading de views (já configurado no router)
   - Confiabilidade: PWA com cache offline
   - Excelência operacional: CI/CD automático (GitHub Pages)
   - Otimização de custos: tudo estático, sem backend na Fase 1
   - Sustentabilidade: código limpo, DRY, componentes reutilizáveis

9. **Boas práticas:**
   - Um commit por feature/fix com mensagem descritiva (conventional commits)
   - Build deve passar (type-check + vite build) antes de push
   - Testar os 3 idiomas mentalmente (textos fazem sentido?)
   - Acessibilidade: labels, contraste, semântica HTML

### Pós-implementação

10. **Atualizar release-notes.json** com a entrada da nova feature/fix/dica
11. **Commitar** com mensagem no formato: `feat:`, `fix:`, `refactor:`, `docs:`
12. **Referenciar a issue** no commit: `Closes #N` ou `Ref: #N`
13. **Push para main**
14. **Fechar a issue** com comentário documentando:
    - O que foi implementado
    - Arquivos modificados
    - Crédito ao autor (se TIP)

---

## Checklist Rápido

```
[ ] Issue analisada e compreendida
[ ] SPEC.md verificada/atualizada
[ ] DESIGN.md verificado/atualizado
[ ] Código segue padrões do projeto
[ ] Textos em PT, EN e ES
[ ] Links externos com rel="noopener noreferrer"
[ ] Build passa (npm run build)
[ ] release-notes.json atualizado
[ ] Commit com conventional commits + referência à issue
[ ] Issue fechada com documentação
```

---

## Referências

- **SPEC.md** — Especificação funcional do sistema
- **DESIGN.md** — Design técnico e arquitetura
- **frontend/src/locales/** — Arquivos de internacionalização
- **frontend/src/data/release-notes.json** — Histórico de releases
- **.github/ISSUE_TEMPLATE/tip.yml** — Template para dicas da comunidade
