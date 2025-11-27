# Voice Commands Reference - Google Maps Assistant

Complete documentation of all voice commands supported by the Portuguese voice-controlled Google Maps assistant.

---

## Table of Contents
1. [Search & Navigation](#search--navigation)
2. [Directions & Routes](#directions--routes)
3. [Trip Information](#trip-information)
4. [Map Controls](#map-controls)
5. [Place Selection](#place-selection)
6. [Location Information](#location-information)
7. [Conversational Commands](#conversational-commands)

---

## Search & Navigation

### Search for a Location
**Intent**: `search_location`
**Handler**: `SearchLocationHandler`

Search for any place, address, or point of interest.

**Example Commands**:
- "Procurar restaurantes perto de Lisboa"
- "Procura Universidade de Aveiro"
- "Encontrar farmácias em Aveiro"
- "Pesquisar Torre Eiffel"
- "Restaurantes perto da Lixa"
- "Cafés no Porto"

**What happens**:
- Closes any open panels
- Types your query in the search box
- Shows search results on the map

**Portuguese Keywords**: procurar, procura, encontrar, pesquisar, mostrar, onde fica

---

### Get Directions
**Intent**: `get_directions`
**Handler**: `GetDirectionsHandler`

Get directions from one location to another.

**Example Commands**:
- "Direções de Lisboa para Porto"
- "Como ir de Aveiro para Coimbra"
- "Rota de casa para o trabalho"
- "Navegar de Portugal para Espanha"
- "Caminho do aeroporto para o hotel"

**What happens**:
- Closes any open panels
- Opens directions panel
- Fills origin and destination
- Calculates route

**Portuguese Keywords**: direções, como ir, rota, navegar, caminho

---

## Directions & Routes

### Change Transport Mode
**Intent**: `change_transport_mode`
**Handler**: `ChangeTransportModeHandler`

Switch between different transportation methods.

**Supported Modes**:
- **Car/Driving**: carro, conduzir, driving, car
- **Walking**: a pé, andar, caminhar, walking
- **Transit**: transportes públicos, autocarro, metro, comboio, transit
- **Cycling**: bicicleta, bike, cycling
- **Two-Wheeler**: mota, scooter, two-wheeler

**Example Commands**:
- "Mudar para carro"
- "Ir a pé"
- "Usar transportes públicos"
- "Mudar para bicicleta"
- "De mota"

**What happens**: Clicks the corresponding transport mode button on Google Maps

---

### Swap Route (Invert Origin/Destination)
**Intent**: `swap_route`
**Handler**: `SwapRouteHandler`

Reverse the direction of your current route.

**Example Commands**:
- "Inverter rota"
- "Trocar origem e destino"
- "Inverter direção"
- "Fazer o caminho inverso"
- "Voltar para trás"

**What happens**: Clicks the swap button to reverse start and end points

---

### Select Alternative Route
**Intent**: `select_alternative_route`
**Handler**: `SelectAlternativeRouteHandler`

Choose from alternative route options shown by Google Maps.

**Example Commands**:
- "Usar rota alternativa"
- "Escolher outra rota"
- "Selecionar rota diferente"
- "Mudar de percurso"
- "Opção alternativa"

**What happens**: Selects a different route option from the available alternatives

---

## Trip Information

### Get Trip Duration
**Intent**: `get_trip_duration`
**Handler**: `GetTripDurationHandler`

Ask how long the current trip will take.

**Example Commands**:
- "Quanto tempo demora?"
- "Qual é a duração?"
- "Quanto tempo leva?"
- "Tempo de viagem"
- "Duração da viagem"

**Response Example**: "A viagem demora aproximadamente 2 horas e 30 minutos"

**What happens**: Extracts duration from the directions panel and speaks it

---

### Get Trip Distance
**Intent**: `get_trip_distance`
**Handler**: `GetTripDistanceHandler`

Ask how far the destination is.

**Example Commands**:
- "Quantos quilómetros?"
- "Qual é a distância?"
- "Quanto é que falta?"
- "Distância total"
- "Quantos metros?"

**Response Example**: "A distância total é de 250 quilómetros"

**What happens**: Extracts distance from the directions panel and speaks it

---

## Map Controls

### Zoom In
**Intent**: `zoom_in`
**Handler**: `ZoomInHandler`

Increase map zoom level (closer view).

**Example Commands**:
- "Aumentar zoom"
- "Mais perto"
- "Aproximar"
- "Zoom in"

**What happens**: Clicks the zoom in (+) button

---

### Zoom Out
**Intent**: `zoom_out`
**Handler**: `ZoomOutHandler`

Decrease map zoom level (wider view).

**Example Commands**:
- "Diminuir zoom"
- "Mais longe"
- "Afastar"
- "Zoom out"

**What happens**: Clicks the zoom out (-) button

---

### Center on Location
**Intent**: `center_location`
**Handler**: `CenterLocationHandler`

Center the map on a specific location.

**Example Commands**:
- "Centrar em Lisboa"
- "Centrar mapa em Aveiro"
- "Focar no Porto"
- "Ir para Coimbra"

**What happens**: Searches for the location and centers the map view on it

---

### Show Traffic
**Intent**: `show_traffic`
**Handler**: `ShowTrafficHandler`

Display traffic layer on the map.

**Example Commands**:
- "Mostrar trânsito"
- "Ativar tráfego"
- "Ver trânsito"
- "Mostrar tráfego"
- "Ligar trânsito"

**What happens**: Enables the traffic layer showing current traffic conditions

---

### Hide Traffic
**Intent**: `hide_traffic`
**Handler**: `HideTrafficHandler`

Remove traffic layer from the map.

**Example Commands**:
- "Esconder trânsito"
- "Desativar tráfego"
- "Remover trânsito"
- "Ocultar tráfego"

**What happens**: Disables the traffic layer

---

### Toggle Satellite View
**Intent**: `toggle_satellite`
**Handler**: `ToggleSatelliteHandler`

Switch between map and satellite view.

**Example Commands**:
- "Mudar para satélite"
- "Vista de satélite"
- "Modo satélite"
- "Ativar satélite"

**What happens**: Toggles between standard map and satellite imagery

---

### Clear/Reset Map
**Intent**: `clear_map`
**Handler**: `ClearMapHandler`

Clear all searches and reset the map to default state.

**Example Commands**:
- "Limpar mapa"
- "Resetar"
- "Limpar pesquisa"
- "Recomeçar"
- "Voltar ao início"

**What happens**: Clears search box, closes all panels, resets map to default view

---

## Place Selection

### Select Place from Results
**Intent**: `select_place`
**Handler**: `SelectPlaceHandler`

Select a specific result from search results list.

**Supported Ordinals**:
- **Portuguese**: primeiro, segundo, terceiro, quarto, quinto, sexto, sétimo, oitavo, nono, décimo
- **English**: first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth
- **Numbers**: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

**Example Commands**:
- "Selecionar o primeiro"
- "Escolher o segundo resultado"
- "Clica no terceiro"
- "Número 5"
- "O quarto"

**What happens**: Clicks on the specified search result in the list

---

## Location Information

### Get Location Details
**Intent**: `get_location_info`
**Handler**: `GetLocationInfoHandler`

Get detailed information about a place.

**Example Commands**:
- "Informações sobre este lugar"
- "Detalhes deste local"
- "O que é este sítio?"
- "Mais informações"
- "Conta-me sobre este lugar"

**What happens**: Extracts and speaks place name, address, rating, and review count

---

### What's Here
**Intent**: `whats_here`
**Handler**: `WhatsHereHandler`

Find out what's at a specific location on the map.

**Example Commands**:
- "O que está aqui?"
- "O que é isto?"
- "Identificar este local"
- "Que lugar é este?"

**What happens**: Right-clicks the map center and shows "What's here" information

---

## Conversational Commands

### Greetings
**Intent**: `greet`
**Handler**: `GreetHandler`

Say hello to the assistant.

**Example Commands**:
- "Olá"
- "Bom dia"
- "Boa tarde"
- "Boa noite"
- "Oi"

**Response**: "Olá! Como posso ajudar com o Google Maps?"

---

### Thank You
**Intent**: `thank_you`
**Handler**: `ThankYouHandler`

Thank the assistant.

**Example Commands**:
- "Obrigado"
- "Obrigada"
- "Muito obrigado"
- "Agradeço"

**Response**: "De nada! Estou aqui para ajudar."

---

### Help
**Intent**: `help`
**Handler**: `HelpHandler`

Get help on what the assistant can do.

**Example Commands**:
- "Ajuda"
- "O que podes fazer?"
- "Quais comandos?"
- "Como usar?"
- "Preciso de ajuda"

**Response**: Lists available command categories and examples

---

## System Behavior

### Welcome Greeting
When you start the system, it automatically greets you:
> "Olá! Assistente de Google Maps pronto. Como posso ajudar?"

### Automatic Panel Closing
The system automatically closes open panels (directions, search results) before executing new commands, so you don't need to manually close anything between commands.

### Error Handling
If something goes wrong, the assistant will speak an error message in Portuguese explaining what happened.

---

## Example Usage Scenarios

### Scenario 1: Planning a Trip
1. **You**: "Direções de Lisboa para Porto"
2. **Assistant**: "A procurar direções de Lisboa para Porto"
3. **You**: "Quanto tempo demora?"
4. **Assistant**: "A viagem demora aproximadamente 3 horas"
5. **You**: "Quantos quilómetros?"
6. **Assistant**: "A distância total é de 314 quilómetros"
7. **You**: "Mostrar trânsito"
8. **Assistant**: "A mostrar trânsito no mapa"

### Scenario 2: Finding a Restaurant
1. **You**: "Procurar restaurantes em Aveiro"
2. **Assistant**: "A procurar restaurantes em Aveiro"
3. **You**: "Selecionar o segundo"
4. **Assistant**: "A selecionar resultado número 2"
5. **You**: "Informações sobre este lugar"
6. **Assistant**: "Restaurante XYZ, Rua ABC, classificação 4.5 estrelas com 200 avaliações"

### Scenario 3: Changing Transport Mode
1. **You**: "Direções de casa para o trabalho"
2. **Assistant**: "A procurar direções de casa para o trabalho"
3. **You**: "Ir a pé"
4. **Assistant**: "Modo de transporte alterado para a pé"
5. **You**: "Quanto tempo demora?"
6. **Assistant**: "A viagem demora aproximadamente 45 minutos"

### Scenario 4: Exploring Alternatives
1. **You**: "Rota de Aveiro para Coimbra"
2. **Assistant**: "A procurar direções de Aveiro para Coimbra"
3. **You**: "Usar rota alternativa"
4. **Assistant**: "A selecionar rota alternativa"
5. **You**: "Inverter rota"
6. **Assistant**: "Origem e destino invertidos"

---

## Tips for Best Results

1. **Speak Clearly**: Use clear Portuguese pronunciation
2. **Be Specific**: Include location names when possible
3. **Wait for Response**: Let the assistant finish speaking before giving the next command
4. **Natural Language**: You can use natural, conversational Portuguese
5. **Multiple Commands**: Give commands one at a time for best results

---

## Technical Notes

- **Language**: All commands are in Portuguese (pt-PT)
- **Voice**: Uses Microsoft Helia Portuguese voice for responses
- **NLU Engine**: Powered by RASA
- **Browser**: Controls Google Maps via Selenium WebDriver
- **Total Commands**: 20+ different intent handlers

---

## File Locations

All intent handlers are located in:
```
Voice/Assistant/application/intent_handlers/
├── search_handler.py          # Search & Directions
├── map_control_handler.py     # Zoom, Traffic, Satellite, Clear
├── trip_info_handler.py       # Duration, Distance, Transport Mode, Swap
├── selection_handler.py       # Select Places & Routes
├── location_info_handler.py   # Location Details, What's Here
└── conversation_handler.py    # Greetings, Thanks, Help
```

RASA training data:
```
Voice/rasaDemo/data/nlu.yml    # All intent examples
```

---

*Last Updated: 2025-11-27*
*System Version: Production Ready*
