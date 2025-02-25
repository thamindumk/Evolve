package com.backend.evolve.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "shop")
@NoArgsConstructor
@AllArgsConstructor
@Data // Lombok for getters, setters, etc.
public class Shop {

    @Id
    @Column(name = "name", length = 20, nullable = false)
    private String name;

    @Column(name = "address", length = 255, nullable = false)
    private String address;

    @Column(name = "phone_number", length = 10)
    private String phoneNumber;

    @Column(name = "logo_link", length = 255, nullable = false)
    private String logoLink;
}