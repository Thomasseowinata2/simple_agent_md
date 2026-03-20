import pyautogui
import time
import random
import sys

# Set confidence level for image detection
CONFIDENCE = 0.8

def random_input_delay():
    """Applies a random delay between 0.1 and 0.2 seconds."""
    time.sleep(random.uniform(0.1, 0.2))

def find_and_click(image_path, action_name, custom_conf=CONFIDENCE, use_gray=True):
    """Tries to find an image on screen and clicks its center if found."""
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=custom_conf, grayscale=use_gray)
        if location is not None:
            random_input_delay()
            pyautogui.click(location)
            print(f"Action: {action_name}")
            return True
    except Exception:
        pass
    return False

def check_battle_state(image_path):
    """Checks if we are in the battle state without clicking it."""
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=0.8, grayscale=False)
        if location is not None:
            return True
    except Exception:
        pass
    return False

def hunt_for_valid_node(node_img_list, enter_img, custom_conf=0.35):
    """Finds nodes of a specific type, clicks them, and checks if 'Enter' appears."""
    for node_img in node_img_list:
        try:
            # Find ALL matches on the screen
            locations = pyautogui.locateAllOnScreen(node_img, confidence=custom_conf, grayscale=True)
            clicked_spots = []
            
            for loc in locations:
                center = pyautogui.center(loc)
                
                # Deduplication: Don't click the exact same spot in the same scan 
                is_duplicate = False
                for spot in clicked_spots:
                    if abs(center.x - spot.x) < 30 and abs(center.y - spot.y) < 30:
                        is_duplicate = True
                        break
                
                if is_duplicate:
                    continue
                    
                clicked_spots.append(center)
                
                # Test the node
                random_input_delay()
                pyautogui.click(center)
                print(f"Testing map node at X:{center.x} Y:{center.y}...")
                
                # Wait 1.5 seconds for the side panel with 'Enter' to slide in
                time.sleep(1.5)
                
                # Check if the Enter button appeared (using grayscale so UI animations don't break it)
                enter_loc = pyautogui.locateCenterOnScreen(enter_img, confidence=0.8, grayscale=True)
                if enter_loc is not None:
                    print("Valid node found! Clicking Enter.")
                    random_input_delay()
                    pyautogui.click(enter_loc)
                    return True 
                    
        except Exception:
            pass 
            
    return False 

def main():
    print("Starting Limbus Auto-Battle Agent...")
    print("Make sure the game is visible on your primary monitor.")
    print("Press Ctrl+C in this terminal to stop the agent.")
    
    # Paths to your cropped template images
    node_boss_img = 'templates/node_boss.png'
    node_sword_img = 'templates/node_sword.png'
    node_chest_img = 'templates/node_chest.png'
    enter_img = 'templates/btn_enter.png'
    battle_btn_img = 'templates/btn_to_battle.png'
    battle_indicator_img = 'templates/battle_indicator.png'
    node_elite = ['templates/node_elite.png', 'templates/node_elite_2.png','templates/node_elite_3.png','templates/node_elite_4.png']  

    card_imgs = ['templates/card_1.png', 'templates/card_2.png', 'templates/card_3.png', 'templates/card_4.png']
    confirm_img = 'templates/btn_confirm.png'

    while True:
        # 1. Check if we are in battle 
        if check_battle_state(battle_indicator_img):
            print("State: In Battle. Executing P + Enter.")
            random_input_delay()
            pyautogui.press('p')
            random_input_delay()
            pyautogui.press('enter')
        
        # 2. Check for Enter Confirmation Button (Grayscale True to ignore UI shine)
        elif find_and_click(enter_img, "Clicked Enter Button", custom_conf=0.8, use_gray=True):
            pass
            
        # 3. Check for Team Selection "To Battle!" Button (Grayscale True to ignore UI shine)
        elif find_and_click(battle_btn_img, "Clicked To Battle Button", custom_conf=0.8, use_gray=True):
            pass

        # 4. Check for Reward Cards 
        else:
            card_found = False
            for card in card_imgs:
                if find_and_click(card, f"Selected Reward Card", custom_conf=0.7, use_gray=True):
                    card_found = True
                    time.sleep(1)
                    find_and_click(confirm_img, "Clicked Confirm Reward Button", custom_conf=0.8, use_gray=True)
                    break 
            
            if card_found:
                time.sleep(2)
                continue

            # 5. Check for Map Nodes 
            node_priority_list = [node_boss_img] + node_elite + [node_sword_img, node_chest_img]
            
            if hunt_for_valid_node(node_priority_list, enter_img, custom_conf=0.45):
                pass
            
        # 2-second delay between every image checking cycle
        time.sleep(2)

if __name__ == "__main__":
    try:
        print("Agent starting in 3 seconds...")
        time.sleep(3)
        main()
    except KeyboardInterrupt:
        print("\nAgent manually stopped by user. Exiting...")
        sys.exit()