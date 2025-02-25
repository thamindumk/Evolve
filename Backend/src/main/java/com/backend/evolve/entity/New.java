package com.backend.evolve.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Entity
@Table(name = "new")
@NoArgsConstructor
@AllArgsConstructor
@Data
public class New {

    @Id
    @Column(name = "product_id", nullable = false)
    private UUID productId;

    @OneToOne
    @JoinColumn(name = "product_id", referencedColumnName = "id", insertable = false, updatable = false)
    private Product product;
}