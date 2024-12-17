package com.example.demo.controller.api;

import com.example.demo.model.Carta;
import com.example.demo.model.Transazione;
import com.example.demo.service.CartaService;
import com.example.demo.service.TransazioneService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CarteController {
	@Autowired
    private CartaService cartaService;//Injection delle dipendenze service per la gestione dell' entity Carta
    @Autowired
    private TransazioneService transazioneService;//Injection delle dipendenze service per la gestione dell' entity Transazione

    @RequestMapping("/admin/setStato/{id}")
    public Carta setStato(@PathVariable int id){

        return cartaService.setStatoById(id);
    }

    @RequestMapping("/getCarta/{id}")
    public Carta getCarta(@PathVariable int id){

        return cartaService.getById(id);
    }

    @RequestMapping("/admin/newCarta/{credito}")
    public Carta newCarta(@PathVariable float credito){

        return cartaService.newCarta(credito);
    }


    @RequestMapping("/newTransazione/{imp}/{ncarta}")
    public Transazione newTransazione(@PathVariable Float imp, @PathVariable Integer ncarta, Authentication authentication){
        
        return transazioneService.newTransazione(imp,ncarta,authentication);
    }
}

