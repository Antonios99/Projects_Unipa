package com.example.demo.configuration;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class MVCController implements WebMvcConfigurer {

	//viene assiciata la richiesta ad una specifica vista da visualizzare.
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/login").setViewName("Login");
        registry.addViewController("/index").setViewName("index");
        registry.addViewController("/").setViewName("index");

    }

}