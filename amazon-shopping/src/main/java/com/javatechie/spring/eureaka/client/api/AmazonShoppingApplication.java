package com.javatechie.spring.eureaka.client.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
//import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;
//
//@SpringBootApplication
//@EnableEurekaClient
//public class AmazonShoppingApplication {
//
//	@Bean
//	@LoadBalanced
//	public RestTemplate getTemplate() {
//		return new RestTemplate();
//	}
//
//	public static void main(String[] args) {
//		SpringApplication.run(AmazonShoppingApplication.class, args);
//	}
//}
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.netflix.ribbon.RibbonClient;

import com.example.ribbonclient.RibbonConfiguration;
 
//@EnableDiscoveryClient
@SpringBootApplication
@RibbonClient(name = "server", configuration = RibbonConfiguration.class)
public class AmazonShoppingApplication {
	
	@Bean
	@LoadBalanced
	public RestTemplate getTemplate() {
		return new RestTemplate();
	}
	
    public static void main(String[] args) {
        SpringApplication.run(AmazonShoppingApplication.class, args);
    }
}