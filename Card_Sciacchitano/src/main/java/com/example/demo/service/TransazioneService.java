package com.example.demo.service;


import com.example.demo.model.Carta;
import com.example.demo.model.Transazione;
import com.example.demo.model.Utente;
import com.example.demo.repository.InterfaceTransazioneRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;


import java.sql.Date;
import java.util.Calendar;


@Service
public class TransazioneService {

    @Autowired
    InterfaceTransazioneRepository transazioneRepository;
    @Autowired
    private CartaService cartaService;

    public Transazione newTransazione(float importo, Integer idCarta, Authentication authentication){
        Carta carta = cartaService.getById(idCarta);

        Calendar cal = Calendar.getInstance();
        Date dataCorrente = new Date(cal.getTimeInMillis());
        MockUserDetail userDetails = (MockUserDetail) authentication.getPrincipal();

        Utente utente=userDetails.getUtente();

        Transazione transazione= new Transazione(importo, dataCorrente, utente, carta);
        
        // trigger del db che gestisce l'aggiornamento delle transazioni
        return transazioneRepository.save(transazione);
    }

    public  Iterable<Transazione> getTransazioni(Authentication authentication) {

    	MockUserDetail userDetails = (MockUserDetail) authentication.getPrincipal();
        Utente utente = userDetails.getUtente();

        if(utente.getRuolo().equals("ADMIN")){
            return transazioneRepository.findAllOrderByIdDesc();

        }
        else if(utente.getRuolo().equals("NEGOZIANTE")) {
            return transazioneRepository.loadUsingUtenteNativeQuery(utente.getId());

        }

        return null;
    }
}