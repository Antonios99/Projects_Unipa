package com.example.demo.service;


import com.example.demo.model.Carta;
import org.springframework.beans.factory.annotation.Autowired;
import com.example.demo.repository.InterfaceCartaService;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import java.util.Optional;
@Service
public class CartaService {

    @Autowired
    InterfaceCartaService Cartarepository;



    public Carta getById(Integer idCarta){

        Optional<Carta> opCarta = Cartarepository.findById(idCarta);
        
        if (opCarta.isEmpty()){
            return null;
        }
        else return opCarta.get();


    }

    public Carta setStatoById(Integer id){

        Carta carta=this.getById(id);

        if(carta.getStato().equals("attiva")){
            carta.setStato("non attiva");
        }
        else if(carta.getStato().equals("non attiva")){
            carta.setStato("attiva");
        }

        Cartarepository.save(carta);

        return carta;
    }

    public Carta newCarta(float credito){

        Carta carta=new Carta(credito,"attiva");
        return Cartarepository.save(carta);

    }

    public Iterable<Carta>  getCarte(Authentication authentication) {

        return Cartarepository.findAll();


    }



}