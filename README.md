# melendeztech.com

Sitio de una página, bilingüe (ES/EN), más la tarjeta digital en `/card/`.
HTML, CSS y un script pequeño. No hay build, no hay dependencias que instalar.

---

## Qué hay adentro

```
index.html        Sitio principal
og.png            Imagen de previsualización (WhatsApp, LinkedIn, iMessage)
favicon.svg
404.html
CNAME             melendeztech.com
robots.txt
sitemap.xml
card/
  index.html      Tarjeta digital — se voltea, descarga vCard, tiene QR
  og.png          Previsualización de la tarjeta
tools/            Generadores de los assets. Pages los ignora.
```

Todos los archivos van en la **raíz** del repo, no dentro de una carpeta.

---

## Publicar

1. Repo **público** (Pages gratis solo publica desde repos públicos).
2. Sube todo respetando la estructura: `card/index.html` tiene que quedar en
   `card/`, no en la raíz. Si arrastras la carpeta completa a la interfaz web
   de GitHub, la estructura se mantiene sola.
3. **Settings → Pages → Build and deployment**: source `Deploy from a branch`,
   branch `main`, folder `/ (root)`. Guardar.
4. **Settings → Pages → Custom domain**: escribe `melendeztech.com` y guarda.
   El archivo `CNAME` ya trae ese valor, así que debe coincidir.
5. Espera el certificado y marca **Enforce HTTPS**.

El DNS ya está configurado y funcionando, así que no hay que tocar el
registrador. Para referencia, los records que están puestos:

| Tipo  | Host  | Valor                     |
| ----- | ----- | ------------------------- |
| A     | `@`   | `185.199.108.153`         |
| A     | `@`   | `185.199.109.153`         |
| A     | `@`   | `185.199.110.153`         |
| A     | `@`   | `185.199.111.153`         |
| CNAME | `www` | `SirMelendezTech.github.io.` |

Una cosa que sí conviene hacer una vez: **Settings → Pages → Verify domain**.
Evita que alguien más pueda amarrar `melendeztech.com` a su propio repo.

---

## Errores que ya nos costaron una vuelta

- **Los archivos de `card/` tienen que llamarse `index.html` y `og.png`.**
  Si suben como `card--index.html`, la URL `/card/` da 404 porque Pages busca
  un `index.html` dentro de la carpeta. El `sitemap.xml` apunta a `/card/`,
  así que Google indexaría ese 404.
- **`og.png` va en la raíz Y en `card/`.** Cada página apunta a su propia
  copia. Si falta, el enlace compartido por WhatsApp sale sin imagen.
- Después de subir, refresca el cache del preview en
  `developers.facebook.com/tools/debug` con `https://melendeztech.com/`.
  Si no, WhatsApp sigue mostrando la versión vieja por días.

---

## Lo que queda pendiente

**LinkedIn.** El bloque está comentado en `index.html`, cerca del final, en la
sección de contacto. Descoméntalo y sustituye `TU-USUARIO` por tu URL real.
Lo dejé apagado a propósito: un enlace roto en vivo es peor que ninguno.

**Correo.** La página anuncia `pedro@melendeztech.com`. Pages no da buzón —
eso necesita un proveedor (Microsoft 365, Google Workspace, o Zoho que es más
barato para empezar) más records MX en el mismo dominio. Los MX conviven sin
problema con los A records de arriba. Monta SPF, DKIM y DMARC de una vez: vas
a mandar correo frío desde este dominio y sin autenticación cae en spam.

**Tarjetas impresas.** Los PDFs actuales dicen "TI". Para regenerarlos con
"IT", corre `tools/card-generator.py` con las fuentes bajadas — instrucciones
en `tools/README.md`.

---

## Cosas que ya están puestas

- Teléfono `787 630 6364` y WhatsApp `17876306364`, en los tres lugares donde
  aparecen.
- Formspree conectado en `xbgjrewg`. El formulario manda por detrás, así que
  el visitante no sale de la página. Trae honeypot contra bots.
- Idioma: arranca en español, cambia a inglés si el navegador está en inglés,
  y recuerda la selección.

Dos frases del copy son promesas, no datos. Si dejan de ser ciertas, cámbialas:
**"Respuesta en menos de 24 h"** (cintillo y sección de contacto) y
**"Llamada de 20 minutos. Gratis."** (paso 01). El punto verde del cintillo
dice que estás tomando clientes nuevos — cuando estés lleno, edita esa línea.

---

## Editar después

Se edita `index.html` directo en GitHub, se hace commit, y el sitio se
reconstruye en menos de un minuto. El copy de los dos idiomas vive junto:

```html
<span class="es">Texto en español</span><span class="en">English text</span>
```

Hay que editar los dos. Si solo cambias uno, la frase desaparece cuando el
visitante cambia de idioma. Son 73 pares en `index.html`.
