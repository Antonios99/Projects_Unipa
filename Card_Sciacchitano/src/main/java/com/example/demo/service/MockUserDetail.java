package com.example.demo.service;

import com.example.demo.model.Utente;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.List;

public class MockUserDetail implements UserDetails {
	private Utente utente;

    public MockUserDetail(Utente utente) {
        this.utente = utente;
    }
    
    public Utente getUtente(){
        return this.utente;
    }

    public Integer getId(){
        return utente.getId();
    }

    public String getRuolo(){
        return utente.getRuolo();
    }
    
    @Override
    public String getPassword() {
        return utente.getPassword();
    }

    @Override
    public String getUsername() {
        return utente.getEmail();
    }
  //-------Metodi di UserDeatails-------
    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {


        return List.of(new SimpleGrantedAuthority(getRuolo()));
    }
}

