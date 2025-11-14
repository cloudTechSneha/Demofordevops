package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AppTest {
    @Test
    void testGreetWithName() {
        assertEquals("Hello, Worlds!", App.greet("Worlds"));
    }

    @Test
    void testGreetNull() {
        assertEquals("Hello, world!", App.greet(null));
    }
}
