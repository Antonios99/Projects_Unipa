package com.example.demo.repository;


import com.example.demo.model.Utente;
import org.springframework.stereotype.Repository;
import org.springframework.data.jpa.repository.JpaRepository;


@Repository
public interface InterfaceUtenteRepository extends JpaRepository<Utente, Integer> {
	 Utente findByEmail(String email);
}


   

