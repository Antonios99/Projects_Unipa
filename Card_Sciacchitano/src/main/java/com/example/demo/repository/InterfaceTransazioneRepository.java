package com.example.demo.repository;

import com.example.demo.model.Transazione;
import org.springframework.stereotype.Repository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;


import java.util.List;

@Repository
public interface InterfaceTransazioneRepository extends CrudRepository<Transazione,Integer>{
	//query che restituisce le transazioni in ordine decresente degli utenti 
	@Query(value="select * from transazioni where cod_utente= ?1 order by transazioni.id_transazione DESC ", nativeQuery=true)
    public List<Transazione> loadUsingUtenteNativeQuery(Integer cod_utente);


    //query per ottenere i dati in modo decrescente
    @Query(value="select * from transazioni  order by transazioni.id_transazione DESC ", nativeQuery=true)
    public List<Transazione> findAllOrderByIdDesc();

}
