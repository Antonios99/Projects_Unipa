package com.example.demo.controller;

import com.example.demo.model.Carta;
import com.example.demo.model.Transazione;
import com.example.demo.service.TransazioneService;
import com.example.demo.service.CartaService;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.ui.Model;


@Controller
public class GestioneController {

    @Autowired
    private TransazioneService transazioneService;//Injection delle dipendenze service per la gestione dell' entity Transazione
    @Autowired
    private CartaService cartaService;//Injection delle dipendenze service per la gestione dell' entity Carta

    //per ADMIN mostriamo tutte le transazioni, per i NEGOZIANTI mostriamo solo le transazioni effettuate
    @RequestMapping("/elencoTransazioni")
    public String  getTransazioni(Authentication authentication, Model model) {

        Iterable<Transazione> transazioni = transazioneService.getTransazioni(authentication);
        model.addAttribute("transazioni", transazioni);

        return "elencoTransazioni";
    }


    @RequestMapping("/elencoCarte")
    public String  getCarte(Authentication authentication, Model model) {

        Iterable<Carta> carte = cartaService.getCarte(authentication);
        model.addAttribute("carte", carte);
        
        return "elencocarte";
    }
}

