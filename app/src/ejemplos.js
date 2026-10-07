/* ============================================================
   DespliegaUML · ejemplos del modo simple
   Cada ejemplo es una historia abierta: un caso cotidiano que
   el estudiante reconoce, con piezas ya colocadas y preguntas
   que invitan a completar el diagrama.
   ============================================================ */

window.EJEMPLOS_SIMPLES = [
  {
    id: "tienda-online",
    nombre: "Tienda online",
    historia: "Una tienda por internet tiene un catálogo de productos, un sistema de caja que cobra y una base de datos donde se guarda todo. El cliente ve el catálogo, pero el catálogo no cobra: necesita la caja.",
    piezas: [
      { nombre: "Catálogo", x: 120, y: 120, estereotipo: "service" },
      { nombre: "Caja", x: 420, y: 120, estereotipo: "service" },
      { nombre: "Base de datos", x: 720, y: 120, estereotipo: "database" }
    ],
    conectores: [
      { desde: 0, hacia: 1, contrato: "HTTP" },
      { desde: 1, hacia: 2, contrato: "TCP" }
    ],
    servidores: [
      { nombre: "Servidor web", x: 200, y: 380, estereotipo: "device" },
      { nombre: "Servidor de datos", x: 640, y: 380, estereotipo: "device" }
    ],
    pregunta: "¿Qué pasa si el catálogo no puede hablar con la caja? ¿Dónde viven estas piezas: en un solo servidor o en dos?"
  },
  {
    id: "reserva-canchas",
    nombre: "Reserva de canchas",
    historia: "Un club reserva canchas de fútbol. El socio pide una cancha, el sistema mira si está libre y la reserva. Si no hay canchas libres, el sistema avisa.",
    piezas: [
      { nombre: "App del socio", x: 120, y: 120, estereotipo: "application" },
      { nombre: "Reservas", x: 420, y: 120, estereotipo: "service" },
      { nombre: "Calendario", x: 720, y: 120, estereotipo: "database" }
    ],
    conectores: [
      { desde: 0, hacia: 1, contrato: "HTTPS" },
      { desde: 1, hacia: 2, contrato: "TCP" }
    ],
    servidores: [
      { nombre: "Celular del socio", x: 120, y: 380, estereotipo: "device" },
      { nombre: "Servidor del club", x: 520, y: 380, estereotipo: "device" }
    ],
    pregunta: "¿Qué pasa si dos socios reservan la misma cancha a la misma hora? ¿Quién decide: la app o el sistema de reservas?"
  },
  {
    id: "biblioteca",
    nombre: "Biblioteca",
    historia: "Una biblioteca presta libros. El lector busca un catálogo, el sistema de préstamos anota quién se lleva qué libro y la base de datos guarda los libros y los lectores.",
    piezas: [
      { nombre: "Catálogo", x: 120, y: 120, estereotipo: "service" },
      { nombre: "Préstamos", x: 420, y: 120, estereotipo: "service" },
      { nombre: "Base de datos", x: 720, y: 120, estereotipo: "database" }
    ],
    conectores: [
      { desde: 0, hacia: 1, contrato: "HTTP" },
      { desde: 1, hacia: 2, contrato: "TCP" }
    ],
    servidores: [
      { nombre: "PC de la biblioteca", x: 200, y: 380, estereotipo: "device" },
      { nombre: "Servidor central", x: 640, y: 380, estereotipo: "device" }
    ],
    pregunta: "¿Qué pasa si el libro ya está prestado? ¿El catálogo lo sabe o tiene que preguntarle a préstamos?"
  },
  {
    id: "restaurante",
    nombre: "Restaurante",
    historia: "Un restaurante toma pedidos en mesa, la cocina los prepara y la caja cobra. El mesero anota el pedido, pero no lo cocina: la cocina lo hace.",
    piezas: [
      { nombre: "Pedido en mesa", x: 120, y: 120, estereotipo: "application" },
      { nombre: "Cocina", x: 420, y: 120, estereotipo: "service" },
      { nombre: "Caja", x: 720, y: 120, estereotipo: "service" }
    ],
    conectores: [
      { desde: 0, hacia: 1, contrato: "HTTP" },
      { desde: 1, hacia: 2, contrato: "HTTP" }
    ],
    servidores: [
      { nombre: "Tablet del mesero", x: 120, y: 380, estereotipo: "device" },
      { nombre: "PC de cocina", x: 420, y: 380, estereotipo: "device" },
      { nombre: "PC de caja", x: 720, y: 380, estereotipo: "device" }
    ],
    pregunta: "¿Qué pasa si la cocina está llena? ¿El mesero sigue tomando pedidos o el sistema le dice que espere?"
  },
  {
    id: "universidad",
    nombre: "Universidad",
    historia: "Una universidad matricula alumnos, les pone notas y emite certificados. El alumno se matricula, pero no se pone notas: el profesor lo hace.",
    piezas: [
      { nombre: "Alumno", x: 120, y: 120, estereotipo: "application" },
      { nombre: "Matrícula", x: 420, y: 120, estereotipo: "service" },
      { nombre: "Notas", x: 720, y: 120, estereotipo: "database" }
    ],
    conectores: [
      { desde: 0, hacia: 1, contrato: "HTTPS" },
      { desde: 1, hacia: 2, contrato: "TCP" }
    ],
    servidores: [
      { nombre: "Celular del alumno", x: 120, y: 380, estereotipo: "device" },
      { nombre: "Servidor académico", x: 520, y: 380, estereotipo: "device" }
    ],
    pregunta: "¿Qué pasa si un alumno se matricula en un curso que ya está lleno? ¿Quién decide: la app o el sistema de matrícula?"
  },
  {
    id: "hospital",
    nombre: "Hospital",
    historia: "Un hospital da citas, el doctor atiende y la farmacia entrega medicamentos. El paciente pide cita, pero no se receta: el doctor lo hace.",
    piezas: [
      { nombre: "Paciente", x: 120, y: 120, estereotipo: "application" },
      { nombre: "Citas", x: 420, y: 120, estereotipo: "service" },
      { nombre: "Historia clínica", x: 720, y: 120, estereotipo: "database" }
    ],
    conectores: [
      { desde: 0, hacia: 1, contrato: "HTTPS" },
      { desde: 1, hacia: 2, contrato: "TCP" }
    ],
    servidores: [
      { nombre: "Celular del paciente", x: 120, y: 380, estereotipo: "device" },
      { nombre: "Servidor del hospital", x: 520, y: 380, estereotipo: "device" }
    ],
    pregunta: "¿Qué pasa si el paciente necesita una cita urgente? ¿El sistema le da la primera libre o le toca esperar?"
  },
  {
    id: "gimnasio",
    nombre: "Gimnasio",
    historia: "Un gimnasio tiene membresías, controla quién entra y reserva máquinas. El socio paga su membresía, pero no entra: el control de acceso lo deja.",
    piezas: [
      { nombre: "App del socio", x: 120, y: 120, estereotipo: "application" },
      { nombre: "Membresías", x: 420, y: 120, estereotipo: "service" },
      { nombre: "Control de acceso", x: 720, y: 120, estereotipo: "service" }
    ],
    conectores: [
      { desde: 0, hacia: 1, contrato: "HTTPS" },
      { desde: 1, hacia: 2, contrato: "TCP" }
    ],
    servidores: [
      { nombre: "Celular del socio", x: 120, y: 380, estereotipo: "device" },
      { nombre: "Servidor del gimnasio", x: 520, y: 380, estereotipo: "device" }
    ],
    pregunta: "¿Qué pasa si la membresía está vencida? ¿El control de acceso lo deja entrar o lo manda a pagar?"
  },
  {
    id: "cine",
    nombre: "Cine",
    historia: "Un cine vende boletos, las salas proyectan películas y la taquilla cobra. El cliente compra un boleto, pero no proyecta: la sala lo hace.",
    piezas: [
      { nombre: "App del cine", x: 120, y: 120, estereotipo: "application" },
      { nombre: "Taquilla", x: 420, y: 120, estereotipo: "service" },
      { nombre: "Salas", x: 720, y: 120, estereotipo: "service" }
    ],
    conectores: [
      { desde: 0, hacia: 1, contrato: "HTTPS" },
      { desde: 1, hacia: 2, contrato: "TCP" }
    ],
    servidores: [
      { nombre: "Celular del cliente", x: 120, y: 380, estereotipo: "device" },
      { nombre: "Servidor del cine", x: 520, y: 380, estereotipo: "device" }
    ],
    pregunta: "¿Qué pasa si la sala está llena? ¿La taquilla sigue vendiendo o le dice al cliente que elija otra función?"
  }
];
