def build_email_template(title, message, highlight=None):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>

    <body style="margin:0; padding:0; background-color:#0f172a; font-family:Arial, sans-serif;">

        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="padding:40px 10px;">
            <tr>
                <td align="center">

                    <!-- CONTAINER -->
                    <table width="600" cellpadding="0" cellspacing="0" border="0"
                        style="background-color:#1e293b; border-radius:12px; overflow:hidden;">

                        <!-- HEADER -->
                        <tr>
                            <td style="padding:30px; text-align:center; background-color:#020617;">
                                <h1 style="margin:0; color:#38bdf8; font-size:28px;">DocNest</h1>
                                <p style="color:#94a3b8; font-size:12px; margin-top:8px;">
                                    Intelligent Document Ecosystem
                                </p>
                            </td>
                        </tr>

                        <!-- CONTENT -->
                        <tr>
                            <td style="padding:30px;">

                                <h2 style="color:#f8fafc; margin-bottom:15px;">
                                    {title}
                                </h2>

                                <p style="color:#cbd5e1; font-size:15px; line-height:1.6;">
                                    {message}
                                </p>

                                {f'''
                                <div style="background-color:#334155; padding:15px; border-left:4px solid #38bdf8; margin-top:20px;">
                                    <strong style="color:#bae6fd;">
                                        {highlight}
                                    </strong>
                                </div>
                                ''' if highlight else ''}

                                <!-- BUTTON -->
                                <div style="text-align:center; margin-top:30px;">
                                    <a href="https://docnest-app-xaduyam6dh5zthla9t9b3e.streamlit.app/"
                                       style="display:inline-block;
                                              padding:14px 28px;
                                              background-color:#3b82f6;
                                              color:#ffffff;
                                              font-size:14px;
                                              font-weight:bold;
                                              text-decoration:none;
                                              border-radius:6px;">
                                        Access Workspace
                                    </a>
                                </div>

                                <!-- FALLBACK LINK -->
                                <p style="color:#64748b; font-size:12px; text-align:center; margin-top:20px;">
                                    If the button doesn’t work, copy this link:<br>
                                    https://docnest-app-gmn5sk4fhhyd5a7av8p6nt.streamlit.app/
                                </p>

                            </td>
                        </tr>

                        <!-- FOOTER -->
                        <tr>
                            <td style="padding:20px; text-align:center; background-color:#020617;">
                                <p style="color:#64748b; font-size:11px; margin:0;">
                                    Secure automated email from DocNest<br>
                                    © 2026 DocNest. All rights reserved.
                                </p>
                            </td>
                        </tr>

                    </table>

                </td>
            </tr>
        </table>

    </body>
    </html>
    """