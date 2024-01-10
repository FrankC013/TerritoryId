use sp_core::crypto::AccountId32;
use sp_runtime::MultiAddress;

// Dependiendo de tus dependencias exactas, estas importaciones pueden variar
use sc_client_api::{Client, BlockchainEvents};
use substrate_subxt::{ClientBuilder, system::*};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Dirección del nodo Substrate
    let url = "ws://localhost:9944";

    // Crear un cliente para interactuar con el nodo Substrate
    let client = ClientBuilder::<Runtime>::new().set_url(url).build().await?;

    // Asumimos que tienes un método en tu módulo para crear una prueba de propiedad
    let claim = vec![0, 1]; // Ejemplo de reclamación
    let call = Call::PoeModule(PoeModule::create_claim(claim)); // Ajusta según tu API

    // Realizar la llamada al módulo
    let extrinsic = client.create_signed(call, AccountId32::from([0u8; 32])).await?;

    // Enviar la transacción
    let tx_hash = client.submit_extrinsic(extrinsic).await?;

    println!("Transacción enviada, hash: {:?}", tx_hash);

    Ok(())
}
