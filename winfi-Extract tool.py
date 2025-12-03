import subprocess
import colorama
from colorama import Fore, Style
import time
import os
import ctypes
import sys
import tempfile
import json
from datetime import datetime
from PIL import Image, ImageDraw
import qrcode

# ==================== Initialize colorama ====================
colorama.init()

# ==================== Console Setup ====================
def setup_console():
    """Setup console window"""
    try:
        os.system("title WiFi Extractor - by D4rk9hackr ")
        os.system("mode con: cols=90 lines=40")
    except:
        pass

# ==================== Banner ====================
def banner():
    print(Fore.CYAN + r"""
  ██████╗ ███████╗███╗   ███╗██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
  ██╔══██╗██╔════╝████╗ ████║██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
  ██║  ██║█████╗  ██╔████╔██║███████║███████║██║     █████╔╝ █████╗  ██████╔╝
  ██║  ██║██╔══╝  ██║╚██╔╝██║██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
  ██████╔╝███████╗██║ ╚═╝ ██║██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
  ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                           
              Interactive WiFi Password Extractor
                  Professional Console Edition
""" + Style.RESET_ALL)
    
    print(Fore.YELLOW + "=" * 80 + Style.RESET_ALL)
    print(Fore.GREEN + "         Select from the menu below:" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 80 + Style.RESET_ALL)

# ==================== Main Menu ====================
def show_menu():
    """Display main menu"""
    print(Fore.CYAN + "\n" + "═" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + "         MAIN MENU " + Style.RESET_ALL)
    print(Fore.CYAN + "═" * 50 + Style.RESET_ALL)
    
    print(Fore.YELLOW + "\n[1] " + Fore.WHITE + " List WiFi networks only")
    print(Fore.YELLOW + "[2] " + Fore.WHITE + " Extract & show passwords")
    print(Fore.YELLOW + "[3] " + Fore.WHITE + " Extract & save to file")
    print(Fore.YELLOW + "[4] " + Fore.WHITE + " Generate QR Codes")
    print(Fore.YELLOW + "[5] " + Fore.WHITE + " Extract specific network")
    print(Fore.YELLOW + "[6] " + Fore.WHITE + " Show system statistics")
    print(Fore.YELLOW + "[7] " + Fore.WHITE + "  Advanced options")
    print(Fore.YELLOW + "[8] " + Fore.WHITE + " Exit")
    
    print(Fore.CYAN + "\n" + "═" * 50 + Style.RESET_ALL)
    
    try:
        choice = input(Fore.GREEN + "\n Select option (1-8): " + Style.RESET_ALL)
        return choice.strip()
    except KeyboardInterrupt:
        return "8"

# ==================== Option 1: List Networks Only ====================
def option_list_networks():
    """List all WiFi networks without passwords"""
    print(Fore.CYAN + "\n[*] Searching for WiFi profiles..." + Style.RESET_ALL)
    
    networks = get_wifi_networks()
    if not networks:
        print(Fore.RED + "[!] No WiFi networks found" + Style.RESET_ALL)
        return
    
    print(Fore.GREEN + f"\n[+] Found {len(networks)} network(s):" + Style.RESET_ALL)
    print(Fore.CYAN + "-" * 60 + Style.RESET_ALL)
    
    for i, ssid in enumerate(networks, 1):
        # Check network status
        stdout, _, _ = run_command(f'netsh wlan show interfaces | findstr /C:"{ssid}"')
        status = "✓" if stdout else ""
        print(Fore.WHITE + f"  [{i:2d}]  {ssid} {status}" + Style.RESET_ALL)
    
    print(Fore.CYAN + "-" * 60 + Style.RESET_ALL)

# ==================== Option 2: Extract & Show ====================
def option_extract_and_show():
    """Extract passwords and display them"""
    print(Fore.CYAN + "\n[*] Extracting WiFi passwords..." + Style.RESET_ALL)
    
    networks = get_wifi_networks()
    if not networks:
        return
    
    results = []
    
    for ssid in networks:
        print(Fore.WHITE + f"\n  🔍 Scanning: {ssid}" + Style.RESET_ALL)
        password = extract_password(ssid)
        
        if password and password != "<NO_PASSWORD>":
            print(Fore.GREEN + f"    ✅ Password: {password}" + Style.RESET_ALL)
            results.append((ssid, password, "✅"))
        else:
            print(Fore.YELLOW + "    ⚠️  No saved password" + Style.RESET_ALL)
            results.append((ssid, "None", "⚠️"))
        
        time.sleep(0.2)
    
    # Show final results
    print(Fore.CYAN + "\n" + "═" * 70 + Style.RESET_ALL)
    print(Fore.GREEN + "                 EXTRACTION RESULTS" + Style.RESET_ALL)
    print(Fore.CYAN + "═" * 70 + Style.RESET_ALL)
    
    for ssid, password, status in results:
        print(Fore.WHITE + f"  {status} {ssid}: {password}" + Style.RESET_ALL)

# ==================== Option 3: Extract & Save ====================
def option_extract_and_save():
    """Extract and save results to file"""
    print(Fore.CYAN + "\n[*] Extracting and saving..." + Style.RESET_ALL)
    
    networks = get_wifi_networks()
    if not networks:
        return
    
    results = []
    successful = 0
    
    print(Fore.YELLOW + "[*] Progress: [" + " " * 30 + "] 0%" + Style.RESET_ALL, end='')
    
    for idx, ssid in enumerate(networks):
        password = extract_password(ssid)
        
        if password and password != "<NO_PASSWORD>":
            successful += 1
            status = "✅"
        else:
            password = "<NO_PASSWORD>"
            status = "⚠️"
        
        results.append({
            'ssid': ssid,
            'password': password,
            'status': status
        })
        
        # Update progress bar
        progress = int((idx + 1) / len(networks) * 30)
        percent = int((idx + 1) / len(networks) * 100)
        print(f"\r{Fore.YELLOW}[*] Progress: [{Fore.GREEN}{'█' * progress}{' ' * (30-progress)}{Fore.YELLOW}] {percent}%{Style.RESET_ALL}", end='')
    
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"wifi_passwords_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("WiFi Password Extractor - Professional Edition\n")
            f.write(f"Date: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
            f.write(f"Total Networks: {len(results)}\n")
            f.write(f"Passwords Extracted: {successful}\n")
            f.write("=" * 60 + "\n\n")
            
            for wifi in results:
                f.write(f"🔹 Network: {wifi['ssid']}\n")
                f.write(f"   Password: {wifi['password']}\n")
                f.write(f"   Status: {wifi['status']}\n")
                f.write("-" * 40 + "\n")
        
        print(Fore.GREEN + f"\n[+] Saved successfully to: {filename}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"[*] Extracted {successful} out of {len(results)} passwords" + Style.RESET_ALL)
        
        # Ask to open file
        open_file = input(Fore.CYAN + "\n🔹 Open file now? (y/n): " + Style.RESET_ALL)
        if open_file.lower() == 'y':
            os.startfile(filename)
    
    except Exception as e:
        print(Fore.RED + f"[!] Save error: {e}" + Style.RESET_ALL)

# ==================== Option 4: Generate QR Codes ====================
def option_generate_qr():
    """Generate QR Codes for networks"""
    print(Fore.CYAN + "\n[*] Generating QR Codes..." + Style.RESET_ALL)
    
    networks = get_wifi_networks()
    if not networks:
        return
    
    qr_dir = os.path.join(tempfile.gettempdir(), "wifi_qr_codes")
    os.makedirs(qr_dir, exist_ok=True)
    
    created = 0
    for ssid in networks:
        password = extract_password(ssid)
        
        if password and password != "<NO_PASSWORD>":
            qr_path = generate_qr_code(ssid, password, qr_dir)
            if qr_path:
                print(Fore.GREEN + f"  ✅ QR created for: {ssid}" + Style.RESET_ALL)
                created += 1
            else:
                print(Fore.YELLOW + f"  ⚠️  Failed QR for: {ssid}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"  ⚠️  Skipping {ssid} (no password)" + Style.RESET_ALL)
    
    print(Fore.GREEN + f"\n[+] Created {created} QR Code(s)")
    print(Fore.YELLOW + f"[*] Location: {qr_dir}" + Style.RESET_ALL)
    
    if created > 0:
        open_dir = input(Fore.CYAN + "\n🔹 Open QR Codes folder? (y/n): " + Style.RESET_ALL)
        if open_dir.lower() == 'y':
            os.startfile(qr_dir)

# ==================== Option 5: Extract Specific Network ====================
def option_extract_specific():
    """Extract specific network"""
    networks = get_wifi_networks()
    if not networks:
        return
    
    print(Fore.GREEN + "\n[*] Available networks:" + Style.RESET_ALL)
    for i, ssid in enumerate(networks, 1):
        print(Fore.WHITE + f"  [{i}] {ssid}" + Style.RESET_ALL)
    
    try:
        choice = input(Fore.CYAN + "\n🔹 Select network number (or 0 to go back): " + Style.RESET_ALL)
        choice = int(choice)
        
        if choice == 0:
            return
        
        if 1 <= choice <= len(networks):
            ssid = networks[choice-1]
            print(Fore.CYAN + f"\n[*] Analyzing: {ssid}" + Style.RESET_ALL)
            
            password = extract_password(ssid)
            
            if password and password != "<NO_PASSWORD>":
                print(Fore.GREEN + f"\n[+]  Successfully extracted!" + Style.RESET_ALL)
                print(Fore.WHITE + f"    Network: {ssid}" + Style.RESET_ALL)
                print(Fore.WHITE + f"    Password: {password}" + Style.RESET_ALL)
                
                # Show additional options
                print(Fore.CYAN + "\n🔹 Additional options:" + Style.RESET_ALL)
                print(Fore.WHITE + "   [1] Copy password to clipboard")
                print(Fore.WHITE + "   [2] Generate QR Code")
                print(Fore.WHITE + "   [3] Test connection")
                print(Fore.WHITE + "   [4] Back to menu" + Style.RESET_ALL)
                
                sub_choice = input(Fore.GREEN + "\n🔹 Select: " + Style.RESET_ALL)
                
                if sub_choice == "1":
                    import pyperclip
                    try:
                        pyperclip.copy(password)
                        print(Fore.GREEN + "    Copied to clipboard" + Style.RESET_ALL)
                    except:
                        print(Fore.YELLOW + "     Could not copy (install pyperclip)" + Style.RESET_ALL)
                
                elif sub_choice == "2":
                    qr_dir = os.path.join(tempfile.gettempdir(), "wifi_qr_codes")
                    os.makedirs(qr_dir, exist_ok=True)
                    qr_path = generate_qr_code(ssid, password, qr_dir)
                    if qr_path:
                        print(Fore.GREEN + f"    QR created: {qr_path}" + Style.RESET_ALL)
                        os.startfile(qr_path)
                
                elif sub_choice == "3":
                    print(Fore.CYAN + "   [*] Testing connection..." + Style.RESET_ALL)
                    test_connection(ssid, password)
            
            else:
                print(Fore.YELLOW + f"\n[!]   No saved password for {ssid}" + Style.RESET_ALL)
        
        else:
            print(Fore.RED + "[!] Invalid number" + Style.RESET_ALL)
    
    except ValueError:
        print(Fore.RED + "[!] Please enter a valid number" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}" + Style.RESET_ALL)

# ==================== Option 6: System Statistics ====================
def option_system_stats():
    """Show system statistics"""
    print(Fore.CYAN + "\n[*] Gathering system information..." + Style.RESET_ALL)
    
    stats = []
    
    # Network count
    networks = get_wifi_networks()
    stats.append(("📶 Saved WiFi Networks", len(networks) if networks else 0))
    
    # System info
    try:
        stdout, _, _ = run_command("systeminfo | findstr /B /C:\"OS Name\" /C:\"OS Version\"")
        for line in stdout.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                stats.append((f"🖥️ {key.strip()}", value.strip()))
    except:
        pass
    
    # Network info
    try:
        stdout, _, _ = run_command("ipconfig | findstr IPv4")
        ip_count = len([line for line in stdout.split('\n') if 'IPv4' in line])
        stats.append(("🌐 Active IP Addresses", ip_count))
    except:
        pass
    
    # WiFi interface info
    try:
        stdout, _, _ = run_command("netsh wlan show interfaces")
        if "State" in stdout:
            lines = stdout.split('\n')
            for line in lines:
                if "State" in line and ":" in line:
                    stats.append(("📡 WiFi Adapter State", line.split(":")[1].strip()))
                    break
    except:
        pass
    
    # Display statistics
    print(Fore.GREEN + "\n" + "═" * 50 + Style.RESET_ALL)
    print(Fore.WHITE + "          📊 SYSTEM STATISTICS" + Style.RESET_ALL)
    print(Fore.GREEN + "═" * 50 + Style.RESET_ALL)
    
    for key, value in stats:
        print(Fore.CYAN + f"  {key}: " + Fore.WHITE + f"{value}" + Style.RESET_ALL)
    
    print(Fore.GREEN + "═" * 50 + Style.RESET_ALL)

# ==================== Option 7: Advanced Options ====================
def option_advanced():
    """Advanced options menu"""
    print(Fore.CYAN + "\n" + "═" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + "        ⚙️  ADVANCED OPTIONS ⚙️" + Style.RESET_ALL)
    print(Fore.CYAN + "═" * 50 + Style.RESET_ALL)
    
    print(Fore.YELLOW + "\n[A] " + Fore.WHITE + "🔍 Export as JSON")
    print(Fore.YELLOW + "[B] " + Fore.WHITE + "📊 Export as CSV")
    print(Fore.YELLOW + "[C] " + Fore.WHITE + "🔄 Clear temporary files")
    print(Fore.YELLOW + "[D] " + Fore.WHITE + "🔒 Check security status")
    print(Fore.YELLOW + "[E] " + Fore.WHITE + "📋 Show command history")
    print(Fore.YELLOW + "[F] " + Fore.WHITE + "🏠 Back to main menu")
    
    print(Fore.CYAN + "\n" + "═" * 50 + Style.RESET_ALL)
    
    choice = input(Fore.GREEN + "\n✨ Select option (A-F): " + Style.RESET_ALL).upper()
    
    if choice == "A":
        export_as_json()
    elif choice == "B":
        export_as_csv()
    elif choice == "C":
        clear_temp_files()
    elif choice == "D":
        check_security()
    elif choice == "E":
        show_command_history()
    else:
        return

# ==================== Helper Functions ====================
def run_command(cmd):
    """Run command and return result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=10
        )
        return result.stdout, result.stderr, result.returncode
    except:
        return "", "", 1

def get_wifi_networks():
    """Get list of WiFi networks"""
    stdout, stderr, code = run_command("netsh wlan show profiles")
    
    if code != 0:
        print(Fore.RED + "[!] Failed to get networks" + Style.RESET_ALL)
        return []
    
    networks = []
    for line in stdout.split('\n'):
        if 'All User Profile' in line:
            try:
                ssid = line.split(':', 1)[1].strip()
                networks.append(ssid)
            except:
                continue
    
    return networks

def extract_password(ssid):
    """Extract password for specific network"""
    stdout, stderr, code = run_command(f'netsh wlan show profile name="{ssid}" key=clear')
    
    if code != 0:
        return None
    
    for line in stdout.split('\n'):
        if 'Key Content' in line:
            try:
                return line.split(':', 1)[1].strip()
            except:
                return None
    
    return None

def generate_qr_code(ssid, password, qr_dir):
    """Generate QR Code"""
    try:
        wifi_string = f"WIFI:T:WPA;S:{ssid};P:{password};;"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(wifi_string)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Clean filename
        safe_name = "".join(c for c in ssid if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"wifi_{safe_name}.png"
        qr_path = os.path.join(qr_dir, filename)
        
        qr_img.save(qr_path)
        return qr_path
    except:
        return None

def test_connection(ssid, password):
    """Test WiFi connection"""
    print(Fore.CYAN + "   [*] Testing connection..." + Style.RESET_ALL)
    # This would require more complex code to actually test
    print(Fore.YELLOW + "   ⚠️  Connection testing requires additional setup" + Style.RESET_ALL)

def export_as_json():
    """Export results as JSON"""
    print(Fore.CYAN + "\n[*] Exporting as JSON..." + Style.RESET_ALL)
    
    networks = get_wifi_networks()
    if not networks:
        return
    
    results = []
    for ssid in networks:
        password = extract_password(ssid)
        results.append({
            "ssid": ssid,
            "password": password if password and password != "<NO_PASSWORD>" else None,
            "timestamp": datetime.now().isoformat()
        })
    
    filename = f"wifi_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(Fore.GREEN + f"[+] Exported to: {filename}" + Style.RESET_ALL)

def export_as_csv():
    """Export results as CSV"""
    print(Fore.CYAN + "\n[*] Exporting as CSV..." + Style.RESET_ALL)
    
    networks = get_wifi_networks()
    if not networks:
        return
    
    filename = f"wifi_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("SSID,Password,Status,Date\n")
        for ssid in networks:
            password = extract_password(ssid)
            status = "EXTRACTED" if password and password != "<NO_PASSWORD>" else "NO_PASSWORD"
            f.write(f'"{ssid}","{password if password else ""}","{status}","{datetime.now().strftime("%Y-%m-%d")}"\n')
    
    print(Fore.GREEN + f"[+] Exported to: {filename}" + Style.RESET_ALL)

def clear_temp_files():
    """Clear temporary files"""
    print(Fore.CYAN + "\n[*] Clearing temporary files..." + Style.RESET_ALL)
    
    qr_dir = os.path.join(tempfile.gettempdir(), "wifi_qr_codes")
    count = 0
    
    if os.path.exists(qr_dir):
        for file in os.listdir(qr_dir):
            try:
                os.remove(os.path.join(qr_dir, file))
                count += 1
            except:
                pass
    
    print(Fore.GREEN + f"[+] Cleared {count} temporary files" + Style.RESET_ALL)

def check_security():
    """Check security status"""
    print(Fore.CYAN + "\n[*] Checking security status..." + Style.RESET_ALL)
    
    # Check if running as admin
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        print(Fore.GREEN + "[✓] Running as Administrator" if is_admin else Fore.YELLOW + "[!] Not running as Administrator" + Style.RESET_ALL)
    except:
        pass
    
    # Check Windows Defender
    try:
        stdout, _, _ = run_command('powershell "Get-MpComputerStatus | Select-Object -ExpandProperty AntivirusEnabled"')
        if "True" in stdout:
            print(Fore.GREEN + "[✓] Windows Defender is active" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "[!] Windows Defender not active" + Style.RESET_ALL)
    except:
        pass

def show_command_history():
    """Show command history"""
    print(Fore.CYAN + "\n[*] Command History:" + Style.RESET_ALL)
    print(Fore.YELLOW + "netsh wlan show profiles")
    print("netsh wlan show profile name=\"SSID\" key=clear")
    print("netsh wlan show interfaces")
    print("ipconfig")
    print("systeminfo" + Style.RESET_ALL)

# ==================== Main Function ====================
def main():
    """Main interactive function"""
    os.system("cls" if os.name == "nt" else "clear")
    setup_console()
    
    # Check for admin rights
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            print(Fore.RED + "[!] Administrator rights required!" + Style.RESET_ALL)
            print(Fore.YELLOW + "[*] Please run as Administrator" + Style.RESET_ALL)
            input(Fore.CYAN + "\nPress ENTER to exit..." + Style.RESET_ALL)
            return
    except:
        pass
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        banner()
        
        choice = show_menu()
        
        if choice == "1":
            option_list_networks()
        elif choice == "2":
            option_extract_and_show()
        elif choice == "3":
            option_extract_and_save()
        elif choice == "4":
            option_generate_qr()
        elif choice == "5":
            option_extract_specific()
        elif choice == "6":
            option_system_stats()
        elif choice == "7":
            option_advanced()
        elif choice == "8":
            print(Fore.CYAN + "\n[*] Goodbye " + Style.RESET_ALL)
            time.sleep(1)
            break
        else:
            print(Fore.RED + "\n[!] Invalid selection!" + Style.RESET_ALL)
            time.sleep(1)
            continue
        
        # Wait before returning to menu
        if choice != "8":
            input(Fore.YELLOW + "\n Press ENTER to return to menu..." + Style.RESET_ALL)

# ==================== Program Start ====================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[!] Program terminated by user" + Style.RESET_ALL)
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n[!] Unexpected error: {e}" + Style.RESET_ALL)
        input(Fore.YELLOW + "\nPress ENTER to exit..." + Style.RESET_ALL)
        sys.exit(1)