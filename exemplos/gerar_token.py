"""
Exemplo de como gerar um token JWT para o LiveKit

Instale as dependências necessárias:
pip install livekit-server-sdk-python python-jose[cryptography]

Uso:
    python gerar_token.py --api-key SUA_API_KEY --api-secret SUA_API_SECRET \
           --identity IDENTIDADE --room NOME_DA_SALA [--nome NOME] [--horas 6]
"""

import argparse
import datetime
import sys
from livekit import AccessToken, VideoGrant

def gerar_token(api_key: str, api_secret: str, identity: str, room_name: str, 
               nome: str = "", horas: int = 6) -> str:
    """
    Gera um token JWT para o LiveKit.
    
    Args:
        api_key: Chave da API do LiveKit
        api_secret: Segredo da API do LiveKit
        identity: Identificador único do participante
        room_name: Nome da sala que o participante deseja acessar
        nome: Nome de exibição do participante (opcional)
        horas: Tempo de expiração do token em horas (padrão: 6)
    
    Returns:
        str: Token JWT gerado
    """
    # Cria as permissões para o token
    grant = VideoGrant(
        room_join=True,
        room=room_name,
        can_publish=True,
        can_subscribe=True,
        can_publish_data=True
    )
    
    # Cria o token com as permissões
    token = AccessToken(
        api_key=api_key,
        api_secret=api_secret,
        identity=identity,
        name=nome,
        grant=grant,
        ttl=datetime.timedelta(hours=horas)
    )
    
    # Gera o token JWT
    return token.to_jwt()

def main():
    parser = argparse.ArgumentParser(description='Gerador de Token JWT para LiveKit')
    parser.add_argument('--api-key', required=True, help='Sua chave de API do LiveKit')
    parser.add_argument('--api-secret', required=True, help='Seu segredo de API do LiveKit')
    parser.add_argument('--identity', required=True, help='Identidade do participante')
    parser.add_argument('--room', required=True, help='Nome da sala')
    parser.add_argument('--nome', default='', help='Nome de exibição do participante (opcional)')
    parser.add_argument('--horas', type=int, default=6, 
                       help='Tempo de expiração em horas (padrão: 6)')
    
    args = parser.parse_args()
    
    try:
        token = gerar_token(
            api_key=args.api_key,
            api_secret=args.api_secret,
            identity=args.identity,
            room_name=args.room,
            nome=args.nome,
            horas=args.horas
        )
        
        print("\n" + "="*50)
        print("TOKEN GERADO COM SUCESSO!")
        print("="*50)
        print(f"\nToken: {token}")
        print(f"\nDetalhes:")
        print(f"- API Key: {args.api_key}")
        print(f"- Identidade: {args.identity}")
        print(f"- Sala: {args.room}")
        print(f"- Nome: {args.nome if args.nome else 'Não informado'}")
        print(f"- Expira em: {args.horas} horas")
        print("\n" + "="*50)
        
    except Exception as e:
        print(f"\nErro ao gerar o token: {str(e)}\n")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
