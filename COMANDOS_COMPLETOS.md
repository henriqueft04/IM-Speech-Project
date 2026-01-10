# Comandos Completos do Projeto IM-Speech

Sistema multimodal para controlo do Google Maps através de **voz** (português), **gestos** (Kinect v2) e **fusão complementar** (voz + gestos).

**Wake Word**: Diga **"maps"** para ativar o reconhecimento de voz.

---

## 📢 Comandos de Voz (Speech)

### 🔍 Pesquisa & Navegação

#### `search_location` - Pesquisar Localização
**Exemplos:**
- "procurar Lisboa"
- "encontrar café perto de mim"
- "onde fica Parque Central"
- "mostra-me restaurantes no Porto"
- "Times Square"
- "localizar posto de gasolina mais próximo"
- "procura Starbucks"
- "encontra pizzarias"
- "mostrar farmácias por perto"
- "aeroporto"
- "ver Oceanário de Lisboa"
- "quero ver Alfama"

#### `get_directions` - Obter Direções
**Exemplos:**
- "direções para casa"
- "como chego ao trabalho"
- "navegar para aeroporto"
- "rota para centro"
- "direções de hotel para praia"
- "leva-me para Estação Central"
- "como chegar ao hospital"
- "ir para Lisboa"
- "ir para Porto"
- "ir para Aveiro"
- "para Coimbra"
- "caminho para Faro"

**Com modo de transporte:**
- "direções para Lisboa de carro"
- "rota para Porto de transportes públicos"
- "navegar para praia a pé"
- "direções de bicicleta para parque"

#### `start_navigation` - Iniciar Navegação
**Exemplos:**
- "iniciar navegação"
- "começar navegação"
- "vamos lá"
- "vai"
- "navegar"
- "começar"

#### `stop_navigation` - Parar Navegação
**Exemplos:**
- "parar navegação"
- "terminar navegação"
- "cancelar rota"
- "sair da navegação"

---

### 🗺️ Controlo do Mapa

#### `zoom_in` - Aproximar Zoom
**Exemplos:**
- "aproximar"
- "mais perto"
- "aproximar muito"
- "aumentar"
- "aumentar zoom"
- "ampliar"

#### `zoom_out` - Afastar Zoom
**Exemplos:**
- "afastar"
- "mais longe"
- "afastar muito"
- "diminuir"
- "diminuir zoom"
- "reduzir"

#### `change_map_type` - Mudar Tipo de Mapa
**Exemplos:**
- "mostrar vista de satélite"
- "mudar para satélite"
- "mudar para terreno"
- "vista normal"
- "mapa padrão"
- "modo satélite"

#### `recenter_map` - Recentrar Mapa
**Exemplos:**
- "recentrar"
- "centrar mapa"
- "ir para a minha localização"
- "onde estou"
- "mostrar a minha localização"
- "centrar em mim"
- "centrar"

#### `show_traffic` - Mostrar Trânsito
**Exemplos:**
- "mostrar trânsito"
- "ativar trânsito"
- "ver tráfego"
- "mostrar tráfego"

#### `hide_traffic` - Esconder Trânsito
**Exemplos:**
- "esconder trânsito"
- "desativar trânsito"
- "remover tráfego"

---

### 📍 Informação de Locais

#### `show_place_details` - Mostrar Detalhes do Local
**Exemplos:**
- "mostrar detalhes"
- "mais informação"
- "fala-me sobre este lugar"
- "o que é esta localização"
- "detalhes sobre Torre Eiffel"
- "informação do lugar"

#### `show_reviews` - Mostrar Avaliações
**Exemplos:**
- "mostrar avaliações"
- "quais são as avaliações"
- "ler avaliações"
- "o que dizem as pessoas"
- "classificações"
- "reviews"
- "opiniões"

#### `show_photos` - Mostrar Fotos
**Exemplos:**
- "mostrar fotos"
- "ver fotos"
- "mostrar imagens"
- "ver imagens"
- "fotos"
- "galeria"
- "fotografias"

#### `get_opening_hours` - Obter Horário
**Exemplos:**
- "horário de abertura"
- "quando abre"
- "a que horas fecha"
- "está aberto"
- "horário de funcionamento"

#### `whats_here` - O Que Há Aqui
**Exemplos:**
- "o que há aqui"
- "que lugar é este"
- "onde estou"
- "que sítio é este"

---

### 🚗 Informação de Viagem

#### `get_trip_duration` - Obter Duração da Viagem
**Exemplos:**
- "quanto tempo demora"
- "duração da viagem"
- "tempo de viagem"
- "quanto tempo até lá"
- "tempo estimado"

#### `get_trip_distance` - Obter Distância
**Exemplos:**
- "qual é a distância"
- "quantos quilómetros"
- "distância até lá"
- "quão longe é"

#### `change_transport_mode` - Mudar Modo de Transporte
**Exemplos:**
- "mudar para carro"
- "modo transportes públicos"
- "ir a pé"
- "modo bicicleta"
- "mudar para autocarro"

#### `swap_route` - Trocar Rota
**Exemplos:**
- "mostrar rota alternativa"
- "trocar rota"
- "outra rota"
- "rota diferente"

---

### 🎯 Seleção

#### `select_place` - Selecionar Local
**Exemplos:**
- "selecionar este"
- "escolher este lugar"
- "este"
- "selecionar"
- "escolher"

#### `select_alternative_route` - Selecionar Rota Alternativa
**Exemplos:**
- "escolher esta rota"
- "usar esta rota"
- "selecionar rota alternativa"

---

### 💬 Conversacional

#### `help` - Ajuda
**Exemplos:**
- "ajuda"
- "o que podes fazer"
- "ajuda-me"
- "comandos"
- "o que posso dizer"

#### `cancel` - Cancelar
**Exemplos:**
- "cancelar"
- "parar"
- "sair"
- "voltar"

#### `thanks` - Agradecer
**Exemplos:**
- "obrigado"
- "obrigada"
- "thanks"
- "muito obrigado"

---

## 🤚 Comandos de Gestos (Kinect v2)

### 🏷️ Filtros de Mapa

| Gesto | Descrição |
|-------|-----------|
| **RESTAURANTS** | Mostrar restaurantes próximos |
| **HOTELS** | Mostrar hotéis próximos |
| **GAS_STATIONS** | Mostrar postos de gasolina |
| **TRANSPORTS** | Mostrar transportes públicos |

---

### 🧭 Navegação do Mapa

| Gesto | Descrição |
|-------|-----------|
| **SWIPE_LEFT** | Mover mapa para a esquerda |
| **SWIPE_RIGHT** | Mover mapa para a direita |
| **SWIPE_UP** | Mover mapa para cima |
| **SWIPE_DOWN** | Mover mapa para baixo |
| **ZOOM_IN** | Aproximar zoom (gesto de pinça) |
| **ZOOM_OUT** | Afastar zoom (gesto de abertura) |

---

### 👁️ Street View

| Gesto | Descrição |
|-------|-----------|
| **ENTER_STREET** | Entrar em Street View |
| **EXIT_STREET** | Sair de Street View |
| **FORWARD** | Avançar em Street View |
| **CAMERA** | Controlar câmara em Street View |

---

### 📋 Navegação de Listas

| Gesto | Descrição |
|-------|-----------|
| **SELECT** | Selecionar item da lista |
| **UP_OPTION** | Mover para opção acima |
| **DOWN_OPTION** | Mover para opção abaixo |

---

## 🔗 Comandos de Fusão Complementar (Voz + Gestos)

**Fusão complementar** permite combinar comandos de voz e gestos **dentro de ~500ms** para executar ações compostas.

### ⚡ Fusões Originais (8 comandos)

#### Zoom In + Direções

| Voz | Gesto | Resultado |
|-----|-------|-----------|
| "aproximar" / "zoom in" | SWIPE_UP | **ZOOM_IN_UP**: Aproxima e move para cima |
| "aproximar" / "zoom in" | SWIPE_DOWN | **ZOOM_IN_DOWN**: Aproxima e move para baixo |
| "aproximar" / "zoom in" | SWIPE_LEFT | **ZOOM_IN_LEFT**: Aproxima e move para esquerda |
| "aproximar" / "zoom in" | SWIPE_RIGHT | **ZOOM_IN_RIGHT**: Aproxima e move para direita |

#### Zoom Out + Direções

| Voz | Gesto | Resultado |
|-----|-------|-----------|
| "afastar" / "zoom out" | SWIPE_UP | **ZOOM_OUT_UP**: Afasta e move para cima |
| "afastar" / "zoom out" | SWIPE_DOWN | **ZOOM_OUT_DOWN**: Afasta e move para baixo |
| "afastar" / "zoom out" | SWIPE_LEFT | **ZOOM_OUT_LEFT**: Afasta e move para esquerda |
| "afastar" / "zoom out" | SWIPE_RIGHT | **ZOOM_OUT_RIGHT**: Afasta e move para direita |

---

### 🆕 Fusões Novas (4 comandos - 2026)

#### 1. Direções de Transportes Públicos
**Combinação**: Voz `get_directions` + Gesto `TRANSPORTS`
**Exemplos:**
- Dizer: "ir para Lisboa" + Fazer gesto: TRANSPORTS
- Dizer: "direções para Porto" + Fazer gesto: TRANSPORTS

**Resultado**: Obtém direções e muda automaticamente para modo de transportes públicos.

---

#### 2. Visão Geral do Tráfego
**Combinação**: Voz `show_traffic` + Gesto `ZOOM_OUT`
**Exemplos:**
- Dizer: "mostrar tráfego" + Fazer gesto: ZOOM_OUT
- Dizer: "ver trânsito" + Fazer gesto: ZOOM_OUT

**Resultado**: Ativa camada de tráfego e afasta zoom para visão geral.

---

#### 3. Filtrar Restaurantes e Centrar
**Combinação**: Gesto `RESTAURANTS` + Voz `recenter_map`
**Exemplos:**
- Fazer gesto: RESTAURANTS + Dizer: "centrar"
- Fazer gesto: RESTAURANTS + Dizer: "recentrar"

**Resultado**: Procura restaurantes próximos e seleciona/centra no primeiro resultado.

---

#### 4. Street View - Avançar Continuamente
**Combinação**: Gesto `FORWARD` + Voz `start_navigation`
**Exemplos:**
- Fazer gesto: FORWARD + Dizer: "avançar"
- Fazer gesto: FORWARD + Dizer: "navegar"

**Resultado**: Avança múltiplas vezes em Street View (movimento contínuo).

---

### 🕐 Redundância (2 comandos)

Ações que podem ser executadas com **voz OU gesto** (redundância = maior robustez):

| Ação | Voz | Gesto | Resultado |
|------|-----|-------|-----------|
| Aproximar | "aproximar" | ZOOM_IN | Aproxima o zoom |
| Afastar | "afastar" | ZOOM_OUT | Afasta o zoom |
| Cancelar | "cancelar" | EXIT_STREET | Cancela ação atual |

---

## 📊 Resumo Estatístico

### Comandos por Modalidade

| Modalidade | Quantidade | Tipos |
|------------|-----------|-------|
| **Voz (Speech)** | 27 intents | Pesquisa, navegação, controlo, informação, conversacional |
| **Gestos (Kinect)** | 17 gestos | Filtros, navegação, Street View, listas |
| **Fusão Complementar** | 12 fusões | 8 originais + 4 novas (2026) |
| **Redundância** | 3 comandos | Zoom in, Zoom out, Cancelar |
| **TOTAL** | 59 comandos | Sistema multimodal completo |

---

## 🎯 Como Usar

### 1. Ativar o Sistema
- Diga: **"maps"** (wake word)
- Aguarde o círculo ficar verde
- Diga o comando de voz

### 2. Voz Apenas
```
User: "maps"
System: [Circle turns green]
User: "ir para Aveiro"
System: "A mostrar direções para Aveiro"
```

### 3. Gesto Apenas
```
User: [Faz gesto ZOOM_IN]
System: [Aproxima o mapa]
```

### 4. Fusão Complementar (Voz + Gesto)
```
User: "maps"
User: "aproximar" + [Faz gesto SWIPE_UP simultaneamente]
System: [Aproxima e move mapa para cima]
```

**Timing**: Os dois inputs (voz + gesto) devem ocorrer dentro de **~500ms** para serem reconhecidos como fusão.

---

## 🚀 Performance

- **Wake word**: ~300-500ms de latência
- **Reconhecimento de voz**: ~1-2s (RASA NLU)
- **Reconhecimento de gesto**: ~100-300ms (Kinect v2)
- **Fusão complementar**: ~500ms janela temporal
- **Direções otimizadas**: ~5-8s (50% mais rápido após otimizações)

---

## 📝 Notas Técnicas

### Intents RASA (27 intents)
1. search_location
2. get_directions
3. start_navigation
4. stop_navigation
5. zoom_in
6. zoom_out
7. change_map_type
8. recenter_map
9. show_traffic
10. hide_traffic
11. show_place_details
12. show_reviews
13. show_photos
14. get_opening_hours
15. whats_here
16. get_trip_duration
17. get_trip_distance
18. change_transport_mode
19. swap_route
20. select_place
21. select_alternative_route
22. help
23. cancel
24. thanks
25. center_location (alias de recenter_map)
26. get_location_info (informação geral de local)
27. nlu_fallback (fallback intent)

### Gestos Kinect (17 gestos)
- 4 filtros de mapa
- 6 navegação do mapa
- 4 Street View
- 3 navegação de listas

### Fusões (12 fusões)
- 8 fusões originais (zoom + direções)
- 4 fusões novas 2026 (direções públicas, tráfego, restaurantes, street view)

---

## 🔧 Troubleshooting

### Voz não reconhece
- Verifique que disse "maps" primeiro
- Fale claramente e alto o suficiente
- Aguarde círculo verde antes de comandar

### Gesto não reconhece
- Certifique-se que está no campo de visão do Kinect
- Faça gestos claros e deliberados
- Verifique logs do Kinect para debugging

### Fusão não funciona
- Voz e gesto devem ocorrer **quase simultaneamente** (~500ms)
- Pratique o timing antes de usar em produção
- Verifique logs do FusionEngine para ver se ambos inputs foram recebidos

---

**Versão**: 2.0
**Data**: 2026-01-10
**Autor**: IM-Speech-Project Team
**Linguagem**: Português (pt-PT)
**Hardware**: Kinect v2, Microfone
**Software**: RASA 3.5, Python 3.9, Selenium, SCXML Fusion Engine
