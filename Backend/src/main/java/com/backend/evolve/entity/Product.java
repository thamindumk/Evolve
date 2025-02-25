package com.backend.evolve.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Entity
@NoArgsConstructor
@AllArgsConstructor
@Data
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", columnDefinition = "UUID", updatable = false, nullable = false)
    private UUID id;

    @Column(nullable = false, length = 255)
    private String title;

    @Column(nullable = false, length = 20)
    private String shop_name;

    @Column(nullable = false, length = 50)
    private String price;

    @Column(nullable = false)
    private boolean availability;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String description;

    @Column(nullable = false, length = 255)
    private String link;

    @Column(columnDefinition = "varchar[]")
    private String[] sizes;

    @Column(columnDefinition = "varchar[]")
    private String[] images;

}

