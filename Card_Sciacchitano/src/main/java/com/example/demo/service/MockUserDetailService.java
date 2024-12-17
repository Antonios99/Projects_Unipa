package com.example.demo.service;

import com.example.demo.model.Utente;
import org.springframework.beans.factory.annotation.Autowired;
import com.example.demo.repository.InterfaceUtenteRepository;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class MockUserDetailService implements UserDetailsService {
	@Autowired
	private InterfaceUtenteRepository utenteRepository;

	public MockUserDetailService(InterfaceUtenteRepository utenteRepository){
	        this.utenteRepository=utenteRepository;
	    }


	    @Override
	    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
	        Utente utente = utenteRepository.findByEmail(email);

	        if (utente != null) {

	            var grantedAuthority = new SimpleGrantedAuthority(utente.getRuolo());

	            return new MockUserDetail(utente);

	        }else{
	            throw new UsernameNotFoundException("Invalid username or password.");
	        }
	    }
	}


