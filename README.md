# Gestión de Turnos API

API REST para gestión de turnos con autenticación, roles, pagos y notificaciones.
Desarrollada con FastAPI, PostgreSQL, Redis y Celery.

## Tecnologías

- **FastAPI** - Framework web
- **PostgreSQL** - Base de datos
- **SQLAlchemy** - ORM
- **Redis** - Cache y broker de colas
- **Celery** - Tareas asíncronas
- **Docker** - Contenedores
- **JWT** - Autenticación
- **pytest** - Testing

## Arquitectura

app/
├── api/routes/       # Endpoints
├── core/             # Config, JWT, seguridad
├── db/               # Sesión y base
├── models/           # Modelos SQLAlchemy
├── repositories/     # Acceso a datos
├── schemas/          # Schemas Pydantic
└── services/         # Lógica de negocio

## ⚙️ Setup

### Requisitos
- Docker y Docker Compose

### Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/Lucia2912/gestion-turnos-api.git
cd gestion-turnos-api
```

2. Crear el archivo `.env`
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/turnos_db
SECRET_KEY=tu_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REDIS_URL=redis://redis:6379/0
```

3. Levantar los contenedores
```bash
docker-compose up -d
```

4. Crear el primer admin
```bash
docker exec -it gestionturnos-api-1 python -m app.db.script.create_admin
```

5. Acceder a la documentación

http://localhost:8000/docs

## Roles

| Rol | Permisos |
|---|---|
| `admin` | Crear providers y admins, ver todos los turnos |
| `client` | Crear, pagar y cancelar sus turnos |
| `provider` | Confirmar turnos asignados |

## Endpoints principales

### Auth
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/auth/register` | Registro público (client) |
| POST | `/auth/login` | Login |
| POST | `/auth/register/admin-create` | Crear usuario con rol (solo admin) |

### Turnos
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/appointments/` | Crear turno |
| GET | `/appointments/` | Listar todos (solo admin) |
| POST | `/appointments/{id}/pay` | Pagar turno |
| PATCH | `/appointments/{id}/cancel` | Cancelar turno |
| PATCH | `/appointments/{id}/confirm` | Confirmar turno (solo provider) |

## Flujo de un turno

Crear (pending) → Pagar → approved (confirmed) / rejected (pending)
→ Cancelar (cancelled)
→ Confirmar por provider (confirmed)

## Tests

```bash
python -m pytest tests/ -v
```

Cobertura actual: **14 tests** cubriendo auth, turnos, pagos y validaciones.

| Módulo | Tests |
|---|---|
| Auth | register, login, duplicados, credenciales inválidas |
| Turnos | crear, solapamiento, cancelar, permisos, provider inválido |
| Pagos | aprobado, rechazado, doble pago, no autorizado |

## Migraciones (Alembic)

Generar una nueva migración:
```bash
docker exec -it gestionturnos-api-1 alembic revision --autogenerate -m "descripcion"
```

Aplicar migraciones:
```bash
docker exec -it gestionturnos-api-1 alembic upgrade head
```

Revertir última migración:
```bash
docker exec -it gestionturnos-api-1 alembic downgrade -1
```

## Notificaciones async (Celery + Redis)

Las notificaciones se procesan de forma asíncrona mediante Celery con Redis como broker.

Eventos que disparan notificaciones:
- Pago aprobado → email de confirmación al cliente
- Turno cancelado → email de cancelación al cliente

> **Nota:** actualmente las notificaciones están simuladas con logs.
> La integración con un servicio real de email (AWS SES o SendGrid) 
> está planificada para la siguiente etapa.

Ver logs del worker:
```bash
docker logs gestionturnos-celery_worker-1
```

## Próximamente
- AWS SES para emails reales
- Deploy en AWS (EC2 + RDS + ElastiCache)