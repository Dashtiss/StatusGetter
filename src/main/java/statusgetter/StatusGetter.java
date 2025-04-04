package statusgetter;

import net.fabricmc.api.ModInitializer;
import net.minecraft.server.MinecraftServer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import java.net.HttpURLConnection;
import java.net.URI;
import java.io.OutputStream;
import java.util.HashMap;
import java.util.Map;
import com.google.gson.Gson;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import net.minecraft.server.world.ServerWorld;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class StatusGetter implements ModInitializer {
    public static final String MOD_ID = "statusgetter";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);
    private static final Path CONFIG_PATH = Paths.get("config/statusgetter.json");
    private static String apiEndpoint = "https://example.com/api/status"; // Default API endpoint

    @Override
    public void onInitialize() {
        LOGGER.info("StatusGetter mod initialized.");

        // Load configuration
        loadConfig();

        // Register a server tick event to collect and send data periodically
        ServerTickEvents.END_SERVER_TICK.register(this::onServerTick);
    }

    private void loadConfig() {
        try {
            if (Files.exists(CONFIG_PATH)) {
                String content = Files.readString(CONFIG_PATH);
                JsonObject config = JsonParser.parseString(content).getAsJsonObject();

                if (config.has("apiEndpoint")) {
                    apiEndpoint = config.get("apiEndpoint").getAsString();
                }
            } else {
                // Create default config if it doesn't exist
                JsonObject defaultConfig = new JsonObject();
                defaultConfig.addProperty("apiEndpoint", apiEndpoint);
                Files.createDirectories(CONFIG_PATH.getParent());
                Files.writeString(CONFIG_PATH, defaultConfig.toString());
            }
        } catch (Exception e) {
            LOGGER.error("Failed to load or create configuration file", e);
        }
    }

    private void onServerTick(MinecraftServer server) {
        try {
            // Collect server statistics
            Map<String, Object> stats = new HashMap<>();

            // General server information
            stats.put("tps", server.getTicks());
            stats.put("players", server.getPlayerManager().getPlayerList().size());
            stats.put("max_players", server.getPlayerManager().getMaxPlayerCount());
            stats.put("motd", server.getServerMotd());
            stats.put("server_version", server.getVersion());
            stats.put("is_hardcore", server.isHardcore());
            stats.put("is_online_mode", server.isOnlineMode());
            stats.put("is_pvp_enabled", server.isPvpEnabled());

            // Memory usage
            stats.put("memory_used", Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory());
            stats.put("memory_max", Runtime.getRuntime().maxMemory());

            // World-specific data
            Map<String, Object> worldsData = new HashMap<>();
            for (ServerWorld world : server.getWorlds()) {
                Map<String, Object> worldData = new HashMap<>();
                worldData.put("loaded_chunks", world.getChunkManager().getLoadedChunkCount());
                worldData.put("loaded_entities", world.iterateEntities().spliterator().getExactSizeIfKnown());
                worldData.put("dimension", world.getRegistryKey().getValue().toString());

                // Add world-specific data to worldsData
                worldsData.put(world.getRegistryKey().getValue().toString(), worldData);
            }
            stats.put("worlds", worldsData);

            // Convert stats to JSON
            Gson gson = new Gson();
            String json = gson.toJson(stats);

            // Send data to the API
            sendToApi(json);
        } catch (Exception e) {
            LOGGER.error("Failed to collect or send server statistics", e);
        }
    }

    private void sendToApi(String json) {
        try {
            URI uri = URI.create(apiEndpoint);
            HttpURLConnection connection = (HttpURLConnection) uri.toURL().openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json; utf-8");
            connection.setDoOutput(true);

            try (OutputStream os = connection.getOutputStream()) {
                byte[] input = json.getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            int responseCode = connection.getResponseCode();
            if (responseCode != HttpURLConnection.HTTP_OK) {
                LOGGER.warn("Failed to send data to API. Response code: " + responseCode);
            }
        } catch (Exception e) {
            LOGGER.error("Error while sending data to API", e);
        }
    }
}