import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os


class LunarFeOAnalyzer:
    def __init__(self, root):
        """
        Inicialização da interface gráfica e configuração inicial
        """
        # Configuração da janela principal
        self.root = root                                           # Armazena referência da janela principal
        self.root.title("Analisador de FeO - Solo Lunar")         # Define título conforme imagem
        self.root.geometry("550x570")                              # Ajusta dimensões para corresponder à interface
        self.root.resizable(0,0)                                    # Defeine que a dimensão da janela é fixa
        self.root.configure(bg="lightgray")                        # Define cor de fundo da janela
        
        # Inicialização das variáveis de imagem
        self.clementine_image = None                               # Variável para armazenar imagem principal
        #self.scale_image = None                                    # Variável para armazenar escala de cores
        
        # Carregamento e validação das imagens
        if not self.load_images():                                 # Chama função de carregamento
            return                                                 # Interrompe inicialização se falhar
        
        # Configuração da interface gráfica
        self.setup_interface()                                     # Chama função de configuração da interface
        
    def load_images(self):
        """
        Carrega e valida as imagens necessárias para a análise
        Retorna True se bem-sucedido, False caso contrário
        """
        try:
            # Verifica se os arquivos de imagem existem
            clementine_path = "clementine.tif"                     # Define caminho da imagem principal
            scale_path = "escala-clementine.jpeg"                   # Define caminho da escala
            
            # Verificação de existência dos arquivos
            if not os.path.exists(clementine_path):                # Verifica se arquivo principal existe
                messagebox.showerror("Erro", f"Arquivo '{clementine_path}' não encontrado.")
                return False
                
            if not os.path.exists(scale_path):                     # Verifica se arquivo de escala existe
                messagebox.showerror("Erro", f"Arquivo '{scale_path}' não encontrado.")
                return False
            
            # Carregamento das imagens
            self.clementine_image = cv2.imread(clementine_path)    # Carrega imagem principal usando OpenCV
            #self.scale_image = cv2.imread(scale_path)              # Carrega escala de cores usando OpenCV
            
            # Validação de carregamento bem-sucedido
            if self.clementine_image is None:                      # Verifica se imagem principal foi carregada
                messagebox.showerror("Erro", f"Falha ao carregar '{clementine_path}'. Verifique se é uma imagem válida.")
                return False
            """    
            if self.scale_image is None:                           # Verifica se escala foi carregada
                messagebox.showerror("Erro", f"Falha ao carregar '{scale_path}'. Verifique se é uma imagem válida.")
                return False
            """
            # Verificação de dimensões mínimas
            height, width = self.clementine_image.shape[:2]        # Obtém dimensões da imagem
            if height < 10 or width < 10:                          # Verifica se dimensões são válidas
                messagebox.showerror("Erro", "Imagem Clementine muito pequena para análise.")
                return False
                
            return True                                            # Retorna True se tudo estiver correto
            
        except Exception as e:                                     # Captura qualquer exceção durante carregamento
            messagebox.showerror("Erro", f"Erro inesperado ao carregar imagens: {str(e)}")
            return False
        
    def setup_interface(self):
        """
        Configuração dos elementos da interface gráfica conforme imagem
        """
        # Seção de Instruções
        instructions_frame = tk.Frame(self.root, bg="lightgray", padx=15, pady=0)  # Frame para instruções
        instructions_frame.pack(fill="none", anchor="w")         # Posiciona frame na janela
        
        # Título da seção Instruções
        instructions_title = tk.Label(instructions_frame, text="Instruções", font=("Arial", 14, "bold"), bg="lightgray")  # Título da seção instruções
        instructions_title.pack(anchor="w")                        # Alinha título à esquerda
        
        # Texto das instruções
        instructions_text = """Entre com as coordenadas geográficas do solo lunar
Intervalo de valores para Norte a Sul: 90 a -90
Intervalo de valores para Oeste a Leste: 180 a -180
Insira apenas números inteiros"""
        
        # Label com instruções
        instructions_label = tk.Label(instructions_frame, text=instructions_text, font=("Arial", 12), bg="lightgray", justify="left")  # Label com texto das instruções
        instructions_label.pack(anchor="w", pady=(0, 0))           # Posiciona com padding superior
        
        # Seção de Coordenadas
        coordinates_frame = tk.Frame(self.root, bg="lightgray", padx=15, pady=0)  # Frame para coordenadas
        coordinates_frame.pack(fill="none", anchor="w")          # Posiciona frame na janela
        
        # Título da seção Coordenadas
        coordinates_title = tk.Label(coordinates_frame, text="Coordenadas", font=("Arial", 14, "bold"), bg="lightgray") # Título da seção coordenadas
        coordinates_title.pack(anchor="w")                         # Alinha título à esquerda
        
        # Campo 1: Valor máximo Norte-Sul
        max_ns_label = tk.Label(coordinates_frame, text="Entre com o valor máximo do eixo Norte-Sul:", font=("Arial", 12), bg="lightgray")  # Label do campo máximo NS
        max_ns_label.pack(anchor="w")                # Posiciona label com padding
        self.max_ns_entry = tk.Entry(coordinates_frame, font=("Arial", 12), width=10)  # Campo entrada máximo NS
        self.max_ns_entry.pack(anchor="w")           # Posiciona campo com padding
        
        # Campo 2: Valor mínimo Norte-Sul
        min_ns_label = tk.Label(coordinates_frame, text="Entre com o valor mínimo do eixo Norte-Sul:", font=("Arial", 12), bg="lightgray")  # Label do campo mínimo NS
        min_ns_label.pack(anchor="w")                      # Posiciona label
        self.min_ns_entry = tk.Entry(coordinates_frame, font=("Arial", 12), width=10)  # Campo entrada mínimo NS
        self.min_ns_entry.pack(anchor="w")           # Posiciona campo com padding
        
        # Campo 3: Valor máximo Oeste-Leste
        max_ol_label = tk.Label(coordinates_frame, text="Entre com o valor máximo do eixo Oeste-Leste:", font=("Arial", 12), bg="lightgray")  # Label do campo máximo OL
        max_ol_label.pack(anchor="w")                      # Posiciona label
        self.max_ol_entry = tk.Entry(coordinates_frame, font=("Arial", 12), width=10)  # Campo entrada máximo OL
        self.max_ol_entry.pack(anchor="w")           # Posiciona campo com padding
        
        # Campo 4: Valor mínimo Oeste-Leste
        min_ol_label = tk.Label(coordinates_frame, text="Entre com o valor mínimo do eixo Oeste-Leste:", font=("Arial", 12), bg="lightgray")  # Label do campo mínimo OL
        min_ol_label.pack(anchor="w")                      # Posiciona label
        self.min_ol_entry = tk.Entry(coordinates_frame, font=("Arial", 12), width=10)  # Campo entrada mínimo OL
        self.min_ol_entry.pack(anchor="w")           # Posiciona campo com padding maior
        
        # Botão Executar
        execute_button = tk.Button(coordinates_frame, text="Executar", 
                                 command=self.execute_analysis,     # Define comando do botão
                                 font=("Arial", 12), width=12)      # Configurações do botão executar
        execute_button.pack(pady=10)                               # Posiciona botão centralizado
        
        # Seção de Resultado
        result_main_frame = tk.Frame(self.root, bg="lightgray")  # Frame principal resultado
        result_main_frame.pack(fill="none", padx=15, anchor="w")  # Posiciona frame expansível
        
        # Título da seção Resultado
        result_title = tk.Label(result_main_frame, text="Resultado", 
                              font=("Arial", 14, "bold"), 
                              bg="lightgray")                       # Título da seção resultado
        result_title.pack(anchor="w")                              # Alinha título à esquerda
        
        # Frame interno para área de resultado
        self.result_frame = tk.Frame(result_main_frame, bg="lightgray")          # Frame interno com borda
        self.result_frame.pack(fill="none", anchor="w")  # Posiciona frame interno
        
        # Mensagem inicial de aguardo
        self.waiting_label = tk.Label(self.result_frame, 
                                    text="Aguardando análise...", 
                                    font=("Arial", 12), bg="lightgray")  # Label de aguardo inicial
        self.waiting_label.pack(pady=2)                           # Posiciona label com padding
        
    def geographic_to_pixel(self, lat, lon, image_height, image_width):
        """
        Conversão de coordenadas geográficas para coordenadas de pixel
        """
        # Conversão latitude (Norte-Sul) para coordenada Y de pixel
        pixel_y = int((90 - lat) * image_height / 180)             # Calcula coordenada Y
        
        # Conversão longitude (Oeste-Leste) para coordenada X de pixel  
        pixel_x = int((lon + 180) * image_width / 360)             # Calcula coordenada X
        
        # Garante que as coordenadas estão dentro dos limites da imagem
        pixel_x = max(0, min(pixel_x, image_width - 1))            # Limita X aos bounds da imagem
        pixel_y = max(0, min(pixel_y, image_height - 1))           # Limita Y aos bounds da imagem
        
        return pixel_x, pixel_y                                    # Retorna coordenadas de pixel
        
    def get_area_average_color(self, image, x1, y1, x2, y2):
        """
        Extrai a cor média de uma área retangular da imagem
        """
        # Obtém dimensões da imagem
        height, width = image.shape[:2]                            # Obtém altura e largura da imagem
        
        # Garante que todas as coordenadas estão dentro dos limites válidos
        x1 = max(0, min(x1, width-1))                              # Limita x1 aos bounds da imagem
        x2 = max(0, min(x2, width-1))                              # Limita x2 aos bounds da imagem
        y1 = max(0, min(y1, height-1))                             # Limita y1 aos bounds da imagem
        y2 = max(0, min(y2, height-1))                             # Limita y2 aos bounds da imagem
        
        # Garante ordem correta das coordenadas
        if x1 > x2:                                                # Se x1 maior que x2
            x1, x2 = x2, x1                                        # Troca valores de x1 e x2
        if y1 > y2:                                                # Se y1 maior que y2
            y1, y2 = y2, y1                                        # Troca valores de y1 e y2
            
        # Verifica se a área é válida
        if x2 - x1 < 1 or y2 - y1 < 1:                             # Se área muito pequena
            x2 = x1 + 1                                            # Define x2 como x1 + 1
            y2 = y1 + 1                                            # Define y2 como y1 + 1
            
        # Extrai a região de interesse
        roi = image[y1:y2, x1:x2]                                  # Corta área específica da imagem
        
        # Calcula a cor média da região
        average_color = np.mean(roi, axis=(0, 1))                  # Calcula média nos eixos 0 e 1
        return average_color                                       # Retorna cor média como array BGR
        
    def compare_with_scale(self, target_color):
        """
        Compara a cor extraída com a escala de cores para determinar o percentual de FeO
        """
        # Converte cor de BGR para RGB
        target_rgb = [target_color[2], target_color[1], target_color[0]]  # Inverte ordem BGR->RGB
        
        # Cores de referência da escala com seus respectivos valores de FeO
        reference_colors = [
            ([30, 60, 255], 0),        # Azul escuro - 0% FeO
            ([0, 120, 255], 2),        # Azul - 2% FeO  
            ([0, 180, 255], 4),        # Azul claro - 4% FeO
            ([0, 220, 200], 6),        # Ciano - 6% FeO
            ([0, 255, 150], 8),        # Verde-azul - 8% FeO
            ([50, 255, 50], 10),       # Verde - 10% FeO
            ([150, 255, 0], 12),       # Verde-amarelo - 12% FeO
            ([220, 220, 0], 14),       # Amarelo - 14% FeO
            ([255, 180, 0], 16),       # Laranja - 16% FeO
            ([255, 120, 0], 18),       # Laranja-avermelhado - 18% FeO
            ([255, 50, 0], 20)         # Vermelho - 20% FeO
        ]
        
        # Encontra a cor mais próxima usando distância euclidiana
        min_distance = float('inf')                                # Inicializa com distância infinita
        closest_feo = 0                                            # Inicializa valor de FeO mais próximo
        
        for ref_color, feo_value in reference_colors:              # Para cada cor e valor FeO
            # Calcula distância euclidiana
            distance = np.sqrt(sum((target_rgb[i] - ref_color[i])**2 for i in range(3)))  # Distância 3D
            if distance < min_distance:                            # Se distância é menor
                min_distance = distance                            # Atualiza distância mínima
                closest_feo = feo_value                            # Atualiza valor FeO mais próximo
                
        return closest_feo                                         # Retorna percentual FeO
        
    def determine_associated_element(self, feo_percentage):
        """
        Determina o elemento associado baseado na concentração de FeO
        """
        if feo_percentage < 8.6:                                   # Se FeO menor que 8.6%
            return "Al (Alumínio) e Pode conter argila"  # Retorna Alumínio
        elif 8.6 <= feo_percentage <= 15.9:                       # Se FeO entre 8.6% e 15.9%
            return "Si (Silício)"   # Retorna Silício
        else:                                                      # Se FeO maior que 15.9%
            return "Ti (Titânio) e Pode conter argila"                             # Retorna Titânio
            
    def validate_input_values(self, max_ns, min_ns, max_ol, min_ol):
        """
        Valida os valores de entrada fornecidos pelo usuário
        """
        # Validação dos intervalos Norte-Sul
        if not (-90 <= min_ns <= max_ns <= 90):                    # Verifica se valores NS estão corretos
            raise ValueError("Valores Norte-Sul devem estar entre -90 e 90, com mínimo ≤ máximo")
            
        # Validação dos intervalos Oeste-Leste  
        if not (-180 <= min_ol <= max_ol <= 180):                  # Verifica se valores OL estão corretos
            raise ValueError("Valores Oeste-Leste devem estar entre -180 e 180, com mínimo ≤ máximo")
            
        # Validação de área mínima
        ns_range = max_ns - min_ns                                 # Calcula amplitude Norte-Sul
        ol_range = max_ol - min_ol                                 # Calcula amplitude Oeste-Leste
        
        if ns_range < 1 or ol_range < 1:                           # Se área muito pequena
            raise ValueError("Área selecionada muito pequena. Mínimo 1 grau em cada direção.")
            
    def execute_analysis(self):
        """
        Executa a análise principal baseada nos dados inseridos pelo usuário
        """
        try:
            # Obtenção dos valores de entrada
            max_ns = int(self.max_ns_entry.get())                  # Converte entrada max NS para inteiro
            min_ns = int(self.min_ns_entry.get())                  # Converte entrada min NS para inteiro  
            max_ol = int(self.max_ol_entry.get())                  # Converte entrada max OL para inteiro
            min_ol = int(self.min_ol_entry.get())                  # Converte entrada min OL para inteiro
            
            # Validação dos valores
            self.validate_input_values(max_ns, min_ns, max_ol, min_ol)  # Valida valores inseridos
                
        except ValueError as e:                                    # Captura erros de valor
            messagebox.showerror("Erro de Entrada", f"Erro nos dados inseridos: {str(e)}")
            return                                                 # Interrompe execução
        except Exception as e:                                     # Captura outros erros
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            return                                                 # Interrompe execução
            
        # Obtenção das dimensões da imagem
        height, width = self.clementine_image.shape[:2]            # Obtém altura e largura
        
        # Conversão de coordenadas geográficas para pixels
        x1, y1 = self.geographic_to_pixel(max_ns, min_ol, height, width)  # Canto superior esquerdo
        x2, y2 = self.geographic_to_pixel(min_ns, max_ol, height, width)  # Canto inferior direito
        
        # Extração da cor média da área
        average_color = self.get_area_average_color(self.clementine_image, x1, y1, x2, y2)  # Cor média
        
        # Determinação do percentual de FeO
        feo_percentage = self.compare_with_scale(average_color)    # % FeO baseado na cor
        
        # Determinação do elemento associado
        associated_element = self.determine_associated_element(feo_percentage)  # Elemento químico
        
        # Exibição dos resultados com coordenadas de entrada e pixel
        self.display_results(feo_percentage, associated_element, average_color, 
                            (max_ns, min_ns, max_ol, min_ol), (x1, y1, x2, y2))  # Passa coordenadas entrada e pixel

        
    def display_results(self, feo_percentage, associated_element, color, coordinates_input, coordinates_pixel):
        """
        Exibe os resultados da análise na interface gráfica incluindo coordenadas de entrada
        """
        # Remove a mensagem de aguardo
        if hasattr(self, 'waiting_label'):                         # Se label de aguardo existe
            self.waiting_label.destroy()                           # Remove label de aguardo
            
        # Limpeza de resultados anteriores
        for widget in self.result_frame.winfo_children():          # Para cada widget no frame
            widget.destroy()                                       # Remove widget
            
        # Resultado da concentração de FeO
        feo_label = tk.Label(self.result_frame, 
                        text=f"Concentração de FeO: {feo_percentage}%", 
                        font=("Arial", 12), bg="lightgray")         # Label resultado FeO
        feo_label.pack(pady=2, anchor="w", padx=10)               # Posiciona label alinhado à esquerda
        
        # Elemento associado
        element_label = tk.Label(self.result_frame, 
                            text=f"Elemento associado: {associated_element}", 
                            font=("Arial", 12), bg="lightgray")     # Label elemento
        element_label.pack(pady=2, anchor="w", padx=10)            # Posiciona label alinhado à esquerda
        
        # Coordenadas geográficas fornecidas pelo usuário
        input_coords_label = tk.Label(self.result_frame, 
                            text=f"Coordenadas fornecidas - Norte-Sul: {coordinates_input[0]} a {coordinates_input[1]}, Oeste-Leste: {coordinates_input[2]} a {coordinates_input[3]}", 
                            font=("Arial", 12), bg="lightgray")        # Informação coordenadas entrada
        input_coords_label.pack(pady=2, anchor="w", padx=10)       # Posiciona info alinhada à esquerda
        
        # Informações técnicas adicionais
        color_info = tk.Label(self.result_frame, 
                            text=f"Cor média analisada (BGR): {color.astype(int)}", 
                            font=("Arial", 12), bg="lightgray")        # Informação cor
        color_info.pack(pady=2, anchor="w", padx=10)               # Posiciona info alinhada à esquerda
    
        # Coordenadas convertidas para pixel
        coord_info = tk.Label(self.result_frame, 
                            text=f"Coordenadas de pixel: ({coordinates_pixel[0]}, {coordinates_pixel[1]}) a ({coordinates_pixel[2]}, {coordinates_pixel[3]})", 
                            font=("Arial", 12), bg="lightgray")        # Informação coordenadas pixel
        coord_info.pack(pady=2, anchor="w", padx=10)               # Posiciona info alinhada à esquerda


def main():
    """
    Função principal para inicializar a aplicação
    """
    root = tk.Tk()                                                 # Cria janela principal
    app = LunarFeOAnalyzer(root)                                   # Cria aplicação
    root.mainloop()                                                # Inicia loop GUI


if __name__ == "__main__":                                         # Execução direta
    main()                                                         # Chama função principal
