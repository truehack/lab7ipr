# Лабораторная работа №7: Observability

## Запуск

```bash
cd telegram-support-observability
docker compose up -d
cat > telegram-support-observability/docker-compose.yml << 'EOF'
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "19090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - observability

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "13001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_INSTALL_PLUGINS=grafana-tempo-datasource
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus
      - tempo
    networks:
      - observability

  tempo:
    image: grafana/tempo:latest
    container_name: tempo
    command: ["-config.file=/etc/tempo-config.yaml"]
    ports:
      - "13200:3200"
      - "14317:4317"
      - "14318:4318"
    volumes:
      - ./tempo/tempo-config.yaml:/etc/tempo-config.yaml
      - tempo_data:/tmp/tempo
    networks:
      - observability

volumes:
  prometheus_data:
  grafana_data:
  tempo_data:

networks:
  observability:
    driver: bridge
