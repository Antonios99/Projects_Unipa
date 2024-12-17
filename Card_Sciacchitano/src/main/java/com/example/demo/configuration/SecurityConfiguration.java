package com.example.demo.configuration;

import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.context.annotation.Bean;
import com.example.demo.repository.InterfaceUtenteRepository;
import com.example.demo.service.MockUserDetailService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;
import org.springframework.security.core.userdetails.UserDetailsService;


@Configuration
@EnableWebSecurity
public class SecurityConfiguration {
	@Autowired
    private InterfaceUtenteRepository utenteRepository;
	
    @Autowired
    private UserDetailsService userDetailsService() {
        return new MockUserDetailService(utenteRepository);
    }


    @Bean
    public static BCryptPasswordEncoder passwordEncoder(){
        return new BCryptPasswordEncoder();
    }


    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {

        http.csrf(csrf -> csrf.disable())
                .authorizeHttpRequests(authorize -> authorize
                		.requestMatchers("/", "/index/", "/getCarta/{id}", "/login/**", "/logo.jpg", "/areaRiservata").permitAll()//Tutti gli utenti autenticati posso accedere(areaRiservata) 
                		.requestMatchers("/admin/**").hasAuthority("ADMIN")
                		.requestMatchers("/**").hasAnyAuthority("ADMIN", "NEGOZIANTE")//gli utenti che sono ADMIN o NEGOZIANTE posso accedere a qualsiasi percorso



                )
                .formLogin(form -> form
                        .loginPage("/login")
                        .defaultSuccessUrl("/areaRiservata", true)//percorso unico predefinito per gli utenti che sono riusciti a fare il login 
                        .failureUrl("/login/error").permitAll()

                )
                //gestione del logout
                .logout((logout) -> logout
                        .logoutRequestMatcher(new AntPathRequestMatcher("/logout"))
                        .permitAll());




        return http.build();
    }

}
