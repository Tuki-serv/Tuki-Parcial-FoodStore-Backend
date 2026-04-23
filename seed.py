"""
Script de seed para desarrollo.
Ejecutar: python seed.py
Crea datos de prueba para demostrar el flujo completo.
"""
from decimal import Decimal
from sqlmodel import Session, SQLModel
from app.core.database import engine
from app.modules.categoria.models import Categoria
from app.modules.ingrediente.models import Ingrediente
from app.modules.producto.models import Producto
from app.modules.producto_categoria.models import ProductoCategoria
from app.modules.producto_ingrediente.models import ProductoIngrediente

def seed():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Categorías
        hamburguesas = Categoria(nombre="Hamburguesas", descripcion="Hamburguesas artesanales")
        bebidas      = Categoria(nombre="Bebidas", descripcion="Bebidas frías y calientes")
        sin_tacc     = Categoria(nombre="Sin TACC", descripcion="Opciones libres de gluten", parent_id=None)
        session.add_all([hamburguesas, bebidas, sin_tacc])
        session.flush()

        # Subcategoría (hija de hamburguesas)
        veganas = Categoria(nombre="Veganas", descripcion="Hamburguesas veganas", parent_id=hamburguesas.id)
        session.add(veganas)
        session.flush()

        # Ingredientes
        pan        = Ingrediente(nombre="Pan brioche",      es_alergeno=True)
        carne      = Ingrediente(nombre="Carne vacuna",     es_alergeno=False)
        queso      = Ingrediente(nombre="Queso cheddar",    es_alergeno=True)
        lechuga    = Ingrediente(nombre="Lechuga",          es_alergeno=False)
        tomate     = Ingrediente(nombre="Tomate",           es_alergeno=False)
        hamburguesa_vegana = Ingrediente(nombre="Medallón vegano", es_alergeno=False)
        session.add_all([pan, carne, queso, lechuga, tomate, hamburguesa_vegana])
        session.flush()

        # Productos
        clasica = Producto(
            nombre="Hamburguesa Clásica",
            descripcion="La clásica con cheddar y lechuga",
            precio_base=Decimal("1500.00"),
            imagenes_url=["https://via.placeholder.com/300"],
            stock_cantidad=50,
        )
        vegana = Producto(
            nombre="Hamburguesa Vegana",
            descripcion="100% plant-based",
            precio_base=Decimal("1800.00"),
            imagenes_url=["https://via.placeholder.com/300"],
            stock_cantidad=30,
        )
        coca = Producto(
            nombre="Coca-Cola 500ml",
            precio_base=Decimal("800.00"),
            stock_cantidad=100,
        )
        session.add_all([clasica, vegana, coca])
        session.flush()

        # Links ProductoCategoria
        session.add(ProductoCategoria(producto_id=clasica.id, categoria_id=hamburguesas.id, es_principal=True))
        session.add(ProductoCategoria(producto_id=vegana.id,  categoria_id=hamburguesas.id, es_principal=True))
        session.add(ProductoCategoria(producto_id=vegana.id,  categoria_id=veganas.id,      es_principal=False))
        session.add(ProductoCategoria(producto_id=vegana.id,  categoria_id=sin_tacc.id,     es_principal=False))
        session.add(ProductoCategoria(producto_id=coca.id,    categoria_id=bebidas.id,      es_principal=True))

        # Links ProductoIngrediente
        session.add(ProductoIngrediente(producto_id=clasica.id, ingrediente_id=pan.id,    es_removible=False))
        session.add(ProductoIngrediente(producto_id=clasica.id, ingrediente_id=carne.id,  es_removible=False))
        session.add(ProductoIngrediente(producto_id=clasica.id, ingrediente_id=queso.id,  es_removible=True))
        session.add(ProductoIngrediente(producto_id=clasica.id, ingrediente_id=lechuga.id,es_removible=True))
        session.add(ProductoIngrediente(producto_id=clasica.id, ingrediente_id=tomate.id, es_removible=True))
        session.add(ProductoIngrediente(producto_id=vegana.id,  ingrediente_id=hamburguesa_vegana.id, es_removible=False))
        session.add(ProductoIngrediente(producto_id=vegana.id,  ingrediente_id=lechuga.id,es_removible=True))

        session.commit()
        print("🌱 Seed OK: 4 categorías, 6 ingredientes, 3 productos creados.")

if __name__ == "__main__":
    seed()