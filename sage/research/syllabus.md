### **Curriculum Overview: Architecting the Empire**
This 4-session intensive is designed to transition you from a script-based developer to a **Distributed Systems Architect**. Using the mechanics of strategy games like *Civilization*, we will build the foundation for a scalable, high-concurrency game server.

---

### **Session 1: The Sovereign State (Microservices & RPC)**
**Module Objective:** Transition from a "Monolith" to a decoupled architecture using gRPC for high-speed communication between game services.

*   **Timed Agenda:**
    *   **[20 min] The Fall of the Monolith:** Discussion on why a single server can’t handle 10,000 players. Justification: Understanding the "bottleneck" in game loops.
    *   **[30 min] Protocol Buffers vs. JSON:** Hands-on coding of a .proto file for a "Unit Move" command. Justification: Low-latency communication is vital for real-time strategy.
    *   **[40 min] Service Discovery Basics:** Using Docker-Compose to spin up a "Map Service" and a "Combat Service." Justification: Building on your Docker basics to manage multi-container systems.
*   **Hobby Integration Activity:** *The Diplomatic Envoy.* Design a gRPC service where the "Trade Service" must request resources from the "Inventory Service." You will define the strict "Treaty" (Schema) that both services must follow to exchange Gold for Iron.
*   **Strategic Alignment:** Backend development for games requires extreme efficiency. Moving away from REST to gRPC introduces you to the high-performance networking required for real-time synchronization.
*   **ELI5 Analogy:** A Monolith is like a city where one person is the Mayor, the General, and the Farmer. If they get sick, everything stops. Microservices are like having specialized leaders—if the Farmer is busy, the General can still move the troops.

---

### **Session 2: The Fog of War (Distributed State & Caching)**
**Module Objective:** Master data consistency and low-latency state management using Redis.

*   **Timed Agenda:**
    *   **[20 min] In-Memory vs. Disk:** Why PostgreSQL is too slow for a "unit click." Justification: Understanding storage latency tiers.
    *   **[40 min] Redis Data Structures for Games:** Using Sorted Sets for Leaderboards and Hashes for Player Stats. Justification: Practical application of Redis beyond simple key-value pairs.
    *   **[30 min] The Cache Invalidation Challenge:** Dealing with "Stale Data" (e.g., a unit appearing in two places at once). Justification: Core distributed systems problem: Consistency vs. Availability.
*   **Hobby Integration Activity:** *The Global Leaderboard.* Implement a Redis-backed ranking system where players earn "Culture Points." You must ensure that when 50 players score simultaneously, the "Hall of Fame" updates in real-time without crashing the database.
*   **Strategic Alignment:** Scalable game servers cannot query a heavy database for every movement. Learning distributed caching is the only way to support a "Massively Multiplayer" environment.
*   **ELI5 Analogy:** Your hard drive is a Library (slow but huge), and Redis is your "Active Hand" (fast but limited). You keep the map you are currently playing on in your hand, not tucked away on a shelf in the back of the library.

---

### **Session 3: The Messenger Guild (Asynchronous Events & Pub/Sub)**
**Module Objective:** Implement event-driven architecture using Message Queues (RabbitMQ/Redis Pub-Sub) to handle non-blocking game logic.

*   **Timed Agenda:**
    *   **[25 min] Synchronous vs. Asynchronous:** Why the "End Turn" button shouldn't make the player wait for the AI to calculate. Justification: Enhancing User Experience through async processing.
    *   **[45 min] Building a Message Bus:** Implementing a "Combat Event" that triggers multiple side-effects (Update XP, Play Sound, Alert Enemy). Justification: Decoupling game logic.
    *   **[30 min] Handling Worker Failure:** What happens if the "XP Calculator" service crashes? Justification: Building resilient, "self-healing" backend systems.
*   **Hobby Integration Activity:** *The Barbarian Raid.* Create an event-driven trigger where a "Barbarian Spawn" event is published. Three different "Watchtower" services must "subscribe" to this event and update their local defense status independently.
*   **Strategic Alignment:** High-scale backends rely on asynchronous tasks to stay responsive. This session teaches you how to manage complex workflows without locking up the main game engine.
*   **ELI5 Analogy:** Instead of the King (the server) personally telling every citizen a law has changed, he posts a notice on the Town Square board. The citizens (services) check the board when they are ready and act on it.

---

### **Session 4: Expanding the Empire (Horizontal Scaling & Load Balancing)**
**Module Objective:** Orchestrate multiple server instances and manage "Sticky Sessions" for player connections.

*   **Timed Agenda:**
    *   **[25 min] Horizontal vs. Vertical Scaling:** Why adding more small servers is better than one giant server. Justification: Understanding cost and fault tolerance.
    *   **[35 min] Load Balancing with Nginx:** Setting up a Round-Robin balancer for game traffic. Justification: Practical skill in traffic management.
    *   **[40 min] The Sharding Challenge:** How to split a world map across three different servers. Justification: Advanced distributed logic for massive game worlds.
*   **Hobby Integration Activity:** *The Multiplayer Expansion.* Use Docker to launch 3 identical "Game Room" containers. Configure a Load Balancer to distribute "Players" (simulated requests) across the rooms, ensuring no single room is overwhelmed by a "Zerg Rush" of traffic.
*   **Strategic Alignment:** This is the "Final Boss" of backend development. Learning to scale horizontally ensures your game server can grow from 10 players to 10,000 without a rewrite.
*   **ELI5 Analogy:** If your restaurant is too full, you don't just build a taller kitchen; you open a second location across town and hire a Host (Load Balancer) to tell people which location has an empty table.