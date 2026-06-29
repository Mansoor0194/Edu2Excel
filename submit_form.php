<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");

// Detect if JSON is expected or sent
$is_json = (isset($_SERVER['HTTP_ACCEPT']) && strpos($_SERVER['HTTP_ACCEPT'], 'application/json') !== false) || 
            (isset($_SERVER['CONTENT_TYPE']) && strpos($_SERVER['CONTENT_TYPE'], 'application/json') !== false);

if ($is_json) {
    header("Content-Type: application/json");
} else {
    header("Content-Type: text/html; charset=UTF-8");
}

// Exit early on preflight OPTIONS requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Ensure it is a POST request
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    if ($is_json) {
        echo json_encode(["success" => false, "message" => "Method Not Allowed"]);
    } else {
        echo "<h2>❌ Method Not Allowed</h2>";
    }
    exit();
}

// Load Environment variables from .env file securely
load_env(__DIR__ . '/.env');

// Retrieve SMTP configuration from env
$smtp_host = getenv('SMTP_HOST') ?: 'ssl://smtp.hostinger.com';
$smtp_port = getenv('SMTP_PORT') ?: 465;
$smtp_user = getenv('SMTP_USER');
$smtp_pass = getenv('SMTP_PASS');
$to_email  = getenv('TO_EMAIL') ?: 'enquiry@edu2excel.com';

if (empty($smtp_user) || empty($smtp_pass)) {
    http_response_code(500);
    if ($is_json) {
        echo json_encode(["success" => false, "message" => "Server Configuration Error: Missing credentials."]);
    } else {
        echo "<h2>❌ Server Configuration Error: Missing credentials.</h2>";
    }
    exit();
}

// Get the raw JSON post data
$raw_data = file_get_contents('php://input');
$data = json_decode($raw_data, true);

// If json_decode fails, fallback to $_POST
if (!$data) {
    $data = $_POST;
}

// Validate basic mandatory fields (handle standard forms and test forms)
$name  = isset($data['name']) ? clean_input($data['name']) : (isset($data['fname']) ? clean_input($data['fname']) : '');
$email = isset($data['email']) ? clean_input($data['email']) : '';
$phone = isset($data['phone']) ? clean_input($data['phone']) : (isset($data['mobile']) ? clean_input($data['mobile']) : '');

if (empty($name) || empty($email) || empty($phone)) {
    http_response_code(400);
    if ($is_json) {
        echo json_encode(["success" => false, "message" => "Name, Email, and Phone number are required."]);
    } else {
        echo "<h2>❌ Name, Email, and Phone number are required.</h2>";
    }
    exit();
}

// Format the Email Subject
$subject = isset($data['subject']) ? clean_input($data['subject']) : "New Inquiry from " . $name;

// Build the HTML email body
$body = '
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 0; background-color: #f6f9fc; }
        .container { max-width: 600px; margin: 20px auto; background: #ffffff; border: 1px solid #eef2f6; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        .header { background-color: #002768; color: #ffffff; padding: 30px 20px; text-align: center; }
        .header h2 { margin: 0; font-size: 24px; font-weight: 700; }
        .content { padding: 30px 20px; }
        .section-title { font-size: 18px; font-weight: 700; color: #BE0B32; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #f0f4f8; padding-bottom: 5px; }
        .data-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        .data-table td { padding: 10px; border-bottom: 1px solid #f0f4f8; vertical-align: top; }
        .data-table td.label { font-weight: bold; color: #556171; width: 35%; }
        .data-table td.value { color: #002768; }
        .message-box { background-color: #f7fafc; border-left: 4px solid #BE0B32; padding: 15px; margin-top: 15px; border-radius: 4px; font-style: italic; }
        .footer { background-color: #f7fafc; text-align: center; padding: 15px; font-size: 12px; color: #a0aec0; border-top: 1px solid #eef2f6; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Edu2Excel Inquiry Details</h2>
        </div>
        <div class="content">
            <div class="section-title">Personal Details</div>
            <table class="data-table">
                <tr>
                    <td class="label">Name</td>
                    <td class="value">' . htmlspecialchars($name) . '</td>
                </tr>
                <tr>
                    <td class="label">Email</td>
                    <td class="value"><a href="mailto:' . htmlspecialchars($email) . '">' . htmlspecialchars($email) . '</a></td>
                </tr>
                <tr>
                    <td class="label">Phone</td>
                    <td class="value"><a href="tel:' . htmlspecialchars($phone) . '">' . htmlspecialchars($phone) . '</a></td>
                </tr>
            </table>

            <div class="section-title">Educational Background</div>
            <table class="data-table">
                <tr>
                    <td class="label">10th Qualification</td>
                    <td class="value">' . (isset($data['10th Education']) ? htmlspecialchars($data['10th Education']) : 'Not specified') . '</td>
                </tr>
                <tr>
                    <td class="label">Post-10th Pathway</td>
                    <td class="value">' . (isset($data['Post-10th Pathway']) ? htmlspecialchars($data['Post-10th Pathway']) : 'Not specified') . '</td>
                </tr>
                <tr>
                    <td class="label">Higher Education</td>
                    <td class="value">' . (isset($data['Higher Education']) ? htmlspecialchars($data['Higher Education']) : 'Not specified') . '</td>
                </tr>
            </table>

            <div class="section-title">Preferences & Budget</div>
            <table class="data-table">
                <tr>
                    <td class="label">Preferred Country</td>
                    <td class="value">' . (isset($data['country']) ? htmlspecialchars($data['country']) : 'Not specified') . '</td>
                </tr>
                <tr>
                    <td class="label">Program Type</td>
                    <td class="value">' . (isset($data['program']) ? htmlspecialchars($data['program']) : 'Not specified') . '</td>
                </tr>
                <tr>
                    <td class="label">Select Budget</td>
                    <td class="value">' . (isset($data['budget']) ? htmlspecialchars($data['budget']) : 'Not specified') . '</td>
                </tr>
            </table>';

if (!empty($data['message'])) {
    $body .= '
            <div class="section-title">Additional Message</div>
            <div class="message-box">
                ' . nl2br(htmlspecialchars($data['message'])) . '
            </div>';
}

$body .= '
        </div>
        <div class="footer">
            This inquiry was sent automatically from the Edu2Excel site.
        </div>
    </div>
</body>
</html>
';

// Send SMTP mail
$mail_sent = send_smtp_email($to_email, $subject, $body, $smtp_user, $smtp_pass, $smtp_host, $smtp_port);

// If SMTP failed, fall back to native PHP mail() (matching user's successful test environment)
if (!$mail_sent) {
    $native_headers = "MIME-Version: 1.0\r\n";
    $native_headers .= "Content-Type: text/html; charset=UTF-8\r\n";
    $native_headers .= "From: Edu2Excel Enquiry <$smtp_user>\r\n";
    $native_headers .= "Reply-To: $email\r\n";
    
    $mail_sent = mail($to_email, $subject, $body, $native_headers);
}

if ($mail_sent) {
    http_response_code(200);
    if ($is_json) {
        echo json_encode(["success" => true, "message" => "Thank you! Your message has been sent successfully."]);
    } else {
        echo "<h2>✅ Email Sent Successfully!</h2>";
    }
} else {
    http_response_code(500);
    if ($is_json) {
        echo json_encode(["success" => false, "message" => "Email failed to send. Please check server error logs."]);
    } else {
        echo "<h2>❌ Email Failed to Send!</h2>";
    }
}

/**
 * Clean user inputs to prevent injection attacks
 */
function clean_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

/**
 * Securely load .env file variables into environment
 */
function load_env($path) {
    if (!file_exists($path)) {
        return;
    }
    $lines = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        if (strpos(trim($line), '#') === 0) {
            continue;
        }
        $parts = explode('=', $line, 2);
        if (count($parts) === 2) {
            $name = trim($parts[0]);
            $value = trim($parts[1]);
            if (!array_key_exists($name, $_SERVER) && !array_key_exists($name, $_ENV)) {
                putenv(sprintf('%s=%s', $name, $value));
                $_ENV[$name] = $value;
                $_SERVER[$name] = $value;
            }
        }
    }
}

/**
 * Socket-based SMTP mail delivery function (RFC 821/2821 compliant)
 */
function send_smtp_email($to, $subject, $body, $smtp_user, $smtp_pass, $smtp_host, $smtp_port) {
    $timeout = 15;
    $socket = @fsockopen($smtp_host, $smtp_port, $errno, $errstr, $timeout);
    if (!$socket) {
        error_log("SMTP Connect Failed to $smtp_host:$smtp_port - Error: $errstr ($errno)");
        return false;
    }

    $get_response = function($socket, $expected_code) {
        $response = "";
        while ($line = fgets($socket, 515)) {
            $response .= $line;
            if (substr($line, 3, 1) == " ") {
                break;
            }
        }
        $code = substr($response, 0, 3);
        if ($code != $expected_code) {
            throw new Exception("Expected code $expected_code, received response: $response");
        }
        return $response;
    };

    try {
        $get_response($socket, "220");

        // Say hello
        $clean_host = str_replace(['ssl://', 'tls://'], '', $smtp_host);
        fwrite($socket, "EHLO " . $clean_host . "\r\n");
        $get_response($socket, "250");

        // Request login auth
        fwrite($socket, "AUTH LOGIN\r\n");
        $get_response($socket, "334");

        // Send base64 username
        fwrite($socket, base64_encode($smtp_user) . "\r\n");
        $get_response($socket, "334");

        // Send base64 password
        fwrite($socket, base64_encode($smtp_pass) . "\r\n");
        $get_response($socket, "235");

        // Mail transaction start
        fwrite($socket, "MAIL FROM: <$smtp_user>\r\n");
        $get_response($socket, "250");

        // Set recipient
        fwrite($socket, "RCPT TO: <$to>\r\n");
        $get_response($socket, "250");

        // Begin mail data payload
        fwrite($socket, "DATA\r\n");
        $get_response($socket, "354");

        // Compile headers
        $headers = "MIME-Version: 1.0\r\n";
        $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
        $headers .= "From: Edu2Excel Enquiry <$smtp_user>\r\n";
        $headers .= "To: <$to>\r\n";
        $headers .= "Subject: =?UTF-8?B?" . base64_encode($subject) . "?=\r\n";
        $headers .= "Date: " . date("r") . "\r\n";
        $headers .= "Message-ID: <" . time() . "-" . md5($to . $subject) . "@edu2excel.com>\r\n\r\n";

        // Dot termination ends SMTP transmission body
        $payload = $headers . $body . "\r\n.\r\n";
        fwrite($socket, $payload);
        $get_response($socket, "250");

        fwrite($socket, "QUIT\r\n");
        fclose($socket);
        return true;
    } catch (Exception $e) {
        @fwrite($socket, "QUIT\r\n");
        @fclose($socket);
        error_log("SMTP Exception: " . $e->getMessage());
        return false;
    }
}
?>
