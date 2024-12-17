package com.example.demo.repository;

import com.example.demo.model.Carta;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface InterfaceCartaService extends CrudRepository<Carta,Integer>{
    //metodi CRUD forniti da spring
}

