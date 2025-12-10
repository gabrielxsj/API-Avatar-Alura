import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

API_URL = "https://last-airbender-api.fly.dev/api/v1/characters"

def personagens(request):
    page = int(request.GET.get("page", 1))
    filtro_elemento = request.GET.get("element", "").strip().lower()

    # Chama a API uma página por vez
    params = {"page": page}
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    personagens_api = response.json()

    api_has_more = len(personagens_api) == 20

    personagens = []
    for p in personagens_api:
        p["id"] = p.get("_id", "")
        personagens.append(p)

    if filtro_elemento:
        palavras = {"agua": "water", "terra": "earth", "fogo": "fire", "ar": "air"}
        chave = palavras.get(filtro_elemento, "")
        if chave:
            personagens = [
                p for p in personagens
                if p.get("affiliation") and chave in p["affiliation"].lower()
            ]

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        html_cards = render_to_string("cards.html", {"personagens": personagens})
        return JsonResponse({"html": html_cards, "has_more": api_has_more})

    return render(request, "personagens.html", {
        "personagens": personagens,
        "page": page,
        "has_more": api_has_more,
        "elemento": filtro_elemento,
    })