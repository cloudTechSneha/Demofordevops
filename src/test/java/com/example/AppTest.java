package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AppTest {
    @Test
    void testGreetWithName() {
        assertEquals("Hello, Alice!", App.greet("Alice"));
    }

    @Test
    void testGreetNull() {
        assertEquals("Hello, world!", App.greet(null));
    }
}
