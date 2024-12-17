package com.example.demo.controller;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import com.example.demo.service.MockUserDetail;
import org.springframework.security.core.Authentication;
import org.springframework.ui.Model;


@Controller
public class LoginController {


    //dopo il login viene controlliamo se l'utente ha il ruolo(ADMIN o NEGOZIANTE) e lo reindirizziamo all'areariservata
    @RequestMapping("/areaRiservata")
    public String getAccessPage(Authentication authentication){

    	MockUserDetail userDetails = (MockUserDetail) authentication.getPrincipal();
        String ruolo=userDetails.getRuolo();
        if (ruolo.equals("NEGOZIANTE") || ruolo.equals("ADMIN")){

            return "areaRiservata";
        }

        return "Login";


    }
    
    
    @RequestMapping("/login/error")
    public String getLoginError(Model model){

        model.addAttribute("error","error" );

        return "Login";


    }
}
