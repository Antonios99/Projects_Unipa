package com.example.demo.model;

import jakarta.persistence.*;

@Entity
@Table(name="carte")
public class Carta {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idCarta;

    @Column(nullable=false)
    private Float   credito;
    
    @Column(nullable=false, length=10)
    private String  stato;

    public Carta(Float credito, String stato) {
        this.credito = credito;
        this.stato = stato;
    }

    public Carta() {//costruttore vuoto

    }

    public Integer getIdCarta() {
        return idCarta;
    }

    public void setIdCarta(Integer idCarta) {
        this.idCarta = idCarta;
    }

    public Float getCredito() {
        return credito;
    }

    public void setCredito(Float credito) {
        this.credito = credito;
    }

    public String getStato() {
        return stato;
    }

    public void setStato(String stato) {
        this.stato = stato;
    }
}
