# Guia de Apresentação - Fusão Multimodal
## Cenário Real: Turista em Lisboa

---

## 🎯 Objetivo da Demonstração

Demonstrar todas as **12 fusões complementares** (voz + gestos) num cenário realista: um turista a explorar Lisboa e a planear uma viagem ao Porto.

**Público-alvo**: Stakeholders, professores, júri de avaliação, conferências

**Duração**: 10-15 minutos

**Hardware necessário**: Kinect v2, microfone, projetor/ecrã grande

---

## 📖 Narrativa do Cenário

**Contexto**: És um turista em Lisboa que quer:
1. Explorar a cidade atual (Lisboa)
2. Encontrar locais de interesse (restaurantes, hotéis)
3. Planear viagem ao Porto usando transportes públicos
4. Explorar virtualmente o destino em Street View

---

## 🎬 Roteiro Completo da Demonstração

### **FASE 1: Exploração Inicial de Lisboa** (3 min)

#### Setup Inicial
- Abrir Google Maps em Lisboa (Praça do Comércio)
- Kinect ativo e a detetar o apresentador
- Sistema pronto para receber comandos

---

#### **Fusão 1: ZOOM_OUT + Tráfego (Nova)**
**Objetivo**: Ver visão geral do tráfego na cidade

**Ação**:
```
1. Dizer: "maps"
2. Dizer: "mostrar tráfego"
3. Simultaneamente fazer gesto: ZOOM_OUT
```

**Resultado esperado**:
- Camada de tráfego ativada
- Zoom afasta para visão geral da cidade
- Vê-se o estado do trânsito em Lisboa

**Narração**:
> "Acabei de chegar a Lisboa e quero ter uma visão geral do tráfego na cidade. Com fusão multimodal, ativo o tráfego e afasto o zoom simultaneamente."

---

### **FASE 2: Procura de Restaurantes** (2 min)

#### **Fusão 2: RESTAURANTS + Centrar (Nova)**
**Objetivo**: Encontrar restaurantes próximos e centrar no melhor

**Ação**:
```
1. Fazer gesto: RESTAURANTS
2. Dizer: "centrar"
   (dentro de 500ms)
```

**Resultado esperado**:
- Filtro de restaurantes aplicado
- Mapa centra no primeiro resultado
- Marcadores de restaurantes visíveis

**Narração**:
> "Tenho fome! Vou procurar restaurantes próximos e centrar automaticamente no primeiro resultado usando fusão de gesto e voz."

---

### **FASE 3: Exploração Detalhada da Área** (3 min)

#### **Fusão 3: ZOOM_IN_UP (Original)**
**Objetivo**: Aproximar e explorar área a norte

**Ação**:
```
1. Dizer: "maps"
2. Dizer: "aproximar"
3. Simultaneamente fazer gesto: SWIPE_UP
```

**Resultado esperado**:
- Zoom aproxima
- Mapa move-se para cima
- Vê-se área a norte em detalhe

**Narração**:
> "Quero explorar a zona a norte em mais detalhe. Com fusão, aproximo e movo o mapa para cima ao mesmo tempo."

---

#### **Fusão 4: ZOOM_IN_RIGHT (Original)**
**Objetivo**: Explorar área a este (zona do Castelo)

**Ação**:
```
1. Dizer: "aproximar"
2. Simultaneamente fazer gesto: SWIPE_RIGHT
```

**Resultado esperado**:
- Zoom aproxima ainda mais
- Mapa move-se para a direita
- Zona do Castelo visível

**Narração**:
> "Interessante! Vou explorar mais para este, onde fica o Castelo de São Jorge."

---

#### **Fusão 5: ZOOM_OUT_LEFT (Original)**
**Objetivo**: Voltar atrás e ver zona oeste

**Ação**:
```
1. Dizer: "afastar"
2. Simultaneamente fazer gesto: SWIPE_LEFT
```

**Resultado esperado**:
- Zoom afasta
- Mapa move-se para a esquerda
- Visão mais abrangente da zona oeste

**Narração**:
> "Deixa-me voltar atrás e ver a zona oeste de Lisboa."

---

#### **Fusão 6: ZOOM_IN_DOWN (Original)**
**Objetivo**: Explorar zona ribeirinha em detalhe

**Ação**:
```
1. Dizer: "aproximar"
2. Simultaneamente fazer gesto: SWIPE_DOWN
```

**Resultado esperado**:
- Zoom aproxima
- Mapa move-se para baixo
- Zona ribeirinha visível em detalhe

**Narração**:
> "Agora quero ver a zona ribeirinha em mais detalhe."

---

### **FASE 4: Planeamento de Viagem ao Porto** (3 min)

#### Setup
- Afastar zoom para ver Portugal
- Preparar para obter direções

---

#### **Fusão 7: Direções + Transportes Públicos (Nova)**
**Objetivo**: Obter direções de comboio/autocarro para Porto

**Ação**:
```
1. Dizer: "maps"
2. Dizer: "ir para Porto"
3. Simultaneamente fazer gesto: TRANSPORTS
```

**Resultado esperado**:
- Direções calculadas Lisboa → Porto
- Modo automaticamente mudado para transportes públicos
- Rotas de comboio/autocarro visíveis

**Narração**:
> "Quero ir ao Porto amanhã. Vou pedir direções e mudar automaticamente para transportes públicos usando fusão."

---

#### **Fusão 8: ZOOM_OUT_UP (Original)**
**Objetivo**: Ver rota completa no mapa

**Ação**:
```
1. Dizer: "afastar"
2. Simultaneamente fazer gesto: SWIPE_UP
```

**Resultado esperado**:
- Zoom afasta
- Mapa move-se para cima
- Rota completa Lisboa-Porto visível

**Narração**:
> "Deixa-me afastar e mover para cima para ver toda a rota."

---

#### **Fusão 9: ZOOM_IN_LEFT (Original)**
**Objetivo**: Ver detalhes de Coimbra (ponto intermédio)

**Ação**:
```
1. Dizer: "aproximar"
2. Simultaneamente fazer gesto: SWIPE_LEFT
```

**Resultado esperado**:
- Zoom aproxima
- Mapa move-se para a esquerda
- Coimbra visível (cidade no meio do caminho)

**Narração**:
> "Vou ver Coimbra, que é uma cidade no meio do caminho."

---

#### **Fusão 10: ZOOM_OUT_RIGHT (Original)**
**Objetivo**: Voltar a ver a rota e focar no Porto

**Ação**:
```
1. Dizer: "afastar"
2. Simultaneamente fazer gesto: SWIPE_RIGHT
```

**Resultado esperado**:
- Zoom afasta
- Mapa move-se para a direita
- Foco no destino (Porto)

**Narração**:
> "Agora vou afastar e mover para a direita para ver melhor o Porto."

---

### **FASE 5: Exploração Virtual do Porto** (4 min)

#### Setup
- Centrar no Porto
- Aproximar numa rua famosa (ex: Avenida dos Aliados)

---

#### Entrar em Street View (comando normal)
**Ação**:
```
Fazer gesto: ENTER_STREET
```

**Narração**:
> "Vou explorar virtualmente o Porto antes de lá ir. Entrando em Street View..."

---

#### **Fusão 11: FORWARD + Navegação Contínua (Nova)**
**Objetivo**: Avançar continuamente pela rua

**Ação**:
```
1. Fazer gesto: FORWARD
2. Dizer: "avançar"
   (dentro de 500ms)
```

**Resultado esperado**:
- Múltiplos avanços automáticos em Street View
- Movimento contínuo pela rua
- Exploração fluida

**Narração**:
> "Perfeito! Com fusão, consigo avançar continuamente pela Avenida dos Aliados sem ter que repetir comandos."

---

#### Rodar e explorar (comandos normais)
**Ação**:
```
Fazer gesto: CAMERA (para rodar vista)
```

**Narração**:
> "Que bonito! Vou rodar a câmara para ver os edifícios históricos."

---

#### Sair de Street View
**Ação**:
```
Fazer gesto: EXIT_STREET
```

**Narração**:
> "Agora volto ao mapa normal."

---

### **FASE 6: Procura de Hotel no Porto** (2 min)

#### **Fusão 12: ZOOM_OUT_DOWN (Original)**
**Objetivo**: Ver zona mais abrangente para encontrar hotéis

**Ação**:
```
1. Dizer: "maps"
2. Dizer: "afastar"
3. Simultaneamente fazer gesto: SWIPE_DOWN
```

**Resultado esperado**:
- Zoom afasta
- Mapa move-se para baixo
- Zona mais ampla do Porto visível

**Narração**:
> "Antes de procurar hotel, vou afastar e ver uma zona mais ampla."

---

#### Filtro de Hotéis (comando normal)
**Ação**:
```
Fazer gesto: HOTELS
```

**Resultado esperado**:
- Hotéis próximos marcados no mapa

**Narração**:
> "Ótimo! Agora vejo vários hotéis disponíveis. Esta fusão multimodal torna a navegação muito mais eficiente!"

---

## ✅ Checklist das 12 Fusões Demonstradas

### Fusões Originais (8):
- [x] **ZOOM_IN_UP** - Fase 3
- [x] **ZOOM_IN_DOWN** - Fase 3
- [x] **ZOOM_IN_LEFT** - Fase 4
- [x] **ZOOM_IN_RIGHT** - Fase 3
- [x] **ZOOM_OUT_UP** - Fase 4
- [x] **ZOOM_OUT_DOWN** - Fase 6
- [x] **ZOOM_OUT_LEFT** - Fase 3
- [x] **ZOOM_OUT_RIGHT** - Fase 4

### Fusões Novas 2026 (4):
- [x] **Direções + Transportes** - Fase 4
- [x] **Tráfego + Zoom Out** - Fase 1
- [x] **Restaurantes + Centrar** - Fase 2
- [x] **Street View Avançar** - Fase 5

---

## 🎨 Dicas de Apresentação

### Antes da Demo
1. **Testar setup** 30 min antes
2. **Calibrar Kinect** corretamente
3. **Testar wake word** várias vezes
4. **Preparar mapa** na localização inicial (Praça do Comércio)
5. **Verificar áudio** do microfone

### Durante a Demo
1. **Falar alto e claro** para o wake word
2. **Gestos deliberados** e visíveis
3. **Narrar cada ação** ANTES de executar
4. **Pausar entre fusões** para audiência processar
5. **Mostrar timing** de 500ms entre voz e gesto
6. **Destacar vantagens** de cada fusão

### Frases-chave para Destacar
- "Isto seria impossível com voz ou gestos sozinhos"
- "Reparem na **simultaneidade** da execução"
- "A fusão **reduz passos** de 2-3 para apenas 1"
- "Isto é **mais intuitivo** do que menus tradicionais"
- "Sistema **robusto** com redundância"

---

## 📊 Pontos Técnicos a Mencionar

### Performance
- Janela temporal de **~500ms** para fusão
- Latência total: **~1-2s** (RASA + Kinect + execução)
- **50% mais rápido** que comandos sequenciais

### Inovação
- **12 fusões complementares** (8 originais + 4 novas)
- **3 comandos redundantes** (robustez)
- **27 intents de voz** + **17 gestos**
- Sistema **SCXML** para gestão de estados

### Arquitetura
- **RASA 3.5** para NLU (português)
- **Kinect v2** para gestos 3D
- **Selenium** para controlo do Google Maps
- **FusionEngine** custom para fusão temporal

---

## 🎯 Mensagem Final

**Conclusão da apresentação**:

> "Demonstrámos hoje um sistema multimodal completo com 12 fusões complementares que tornam a interação com mapas mais **natural**, **rápida** e **intuitiva**. A fusão de voz e gestos não é apenas uma novidade tecnológica - é uma forma genuinamente **melhor** de interagir com sistemas complexos como o Google Maps."

> "Este projeto mostra que o futuro da interação humano-computador está na **combinação inteligente** de múltiplas modalidades, não na substituição de umas por outras."

---

## 📝 Backup Plan

### Se algo falhar:

#### Kinect não reconhece gesto:
- Repetir gesto mais devagar
- Verificar posição relativa ao sensor
- Usar gesto alternativo redundante

#### Voz não reconhece:
- Repetir wake word "maps"
- Falar mais alto e claro
- Verificar círculo verde antes de comandar

#### Fusão não ocorre:
- Explicar que timing de 500ms é crítico
- Demonstrar comandos separados primeiro
- Tentar novamente com melhor sincronização

#### Internet lenta:
- Ter screenshots/vídeos de backup
- Explicar fluxo teoricamente
- Mostrar logs do sistema como prova

---

## 🎥 Opções Adicionais

### Para apresentação mais longa (20-30 min):
- Adicionar métricas de **performance** ao vivo
- Mostrar **código SCXML** do FusionEngine
- Demonstrar **training data** do RASA
- Comparar com sistemas **sem fusão**
- Q&A interativo com audiência

### Para apresentação mais curta (5-7 min):
- Focar apenas nas **4 fusões novas**
- Demonstração rápida sem narração detalhada
- Slides com overview técnico

---

## 📈 Métricas a Apresentar (Slide Final)

| Métrica | Valor |
|---------|-------|
| Total de comandos | 59 |
| Fusões complementares | 12 |
| Comandos de voz | 27 intents |
| Gestos Kinect | 17 gestos |
| Comandos redundantes | 3 |
| Janela temporal fusão | ~500ms |
| Latência média | 1-2s |
| Ganho de velocidade | 50% |
| Língua | Português (pt-PT) |
| Precisão RASA | >90% |
| Taxa reconhecimento Kinect | >85% |

---

**Boa sorte com a apresentação! 🚀**

*Lembra-te: A chave é mostrar que a fusão multimodal é **natural**, **eficiente** e **útil** - não apenas tecnologia pela tecnologia.*
